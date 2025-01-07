import os
import io
import csv
import gzip
import boto3
import pandas as pd
import polars as pl
from typing import Tuple, Dict, List
import botocore

from botocore.config import Config
from botocore.client import ClientError
from .. import decorator_manager


def upload_raw_s3(local_folder_path: str, uuid: str) -> None:
    """
    Function upload_raw_s3.
    Use this function to upload raw data to s3.

    Parameters:
          local_folder_path(str): The path of local folder which contains files.
          uuid(str): The uuid for folder data.
    Examples:
        >>> from rcd_dev_kit import database_manager
        >>> database_manager.upload_raw_s3(local_folder_path="my_folder", uuid="my_uuid")
    """
    lst_obj = [obj for obj in os.listdir(local_folder_path) if not obj.startswith(".")]
    lst_local_file = [
        obj for obj in lst_obj if os.path.isfile(os.path.join(local_folder_path, obj))
    ]
    if len(lst_obj) != len(lst_local_file):
        raise TypeError(f"⚠️{set(lst_obj) - set(lst_local_file)} are not files!")

    so = S3Operator()
    so.bucket = os.environ.get("S3_BUCKET_RAW")
    if so.bucket is None:
        raise ValueError(f"Raw Bucket is not defined in .env")
    so.prefix = uuid
    exist = so.detect_prefix()
    if exist:
        lst_s3_files = [
            file_name
            for file in so.list_s3_obj()
            if (file_name := file.split("/")[-1]) != ""
        ]
        diff_to_upload = list(set(lst_local_file) - set(lst_s3_files))
        print(f"✨Uploading {len(diff_to_upload)} new files: {diff_to_upload}")
    else:
        diff_to_upload = lst_local_file
        print(f"📤Uploading {len(diff_to_upload)} files.")
    for file in diff_to_upload:
        so.send_to_s3_file(
            local_file_path=os.path.join(local_folder_path, file),
            s3_file_path=os.path.join(so.prefix, file),
        )


def download_raw_s3(local_folder_path: str, uuid: str) -> None:
    """
    Function download_from_s3.
    Use this function to download data from s3.

    Parameters:
           local_folder_path(str): The path of local folder which contains files.
           uuid(str): The uuid for folder data.
    Examples:
        >>> from rcd_dev_kit import database_manager
        >>> database_manager.download_raw_s3(local_folder_path="my_folder", uuid="my_uuid")
    """
    lst_obj = [obj for obj in os.listdir(local_folder_path) if not obj.startswith(".")]
    lst_local_file = [
        obj for obj in lst_obj if os.path.isfile(os.path.join(local_folder_path, obj))
    ]

    so = S3Operator()
    so.bucket = os.environ.get("S3_BUCKET_RAW")
    if so.bucket is None:
        raise ValueError(f"❌Raw Bucket is not defined in .env")
    so.prefix = uuid
    exist = so.detect_prefix()
    if exist:
        lst_s3_files = [
            file_name
            for file in so.list_s3_obj()
            if (file_name := file.split("/")[-1]) != ""
        ]
        diff_to_download = list(set(lst_s3_files) - set(lst_local_file))
        print(f"📥Downloading {len(diff_to_download)} new files: {diff_to_download}")
        for file in diff_to_download:
            so.download_s3_obj(
                local_file_path=os.path.join(local_folder_path, file),
                s3_file_path=os.path.join(so.prefix, file),
            )
    else:
        print(f"⚠️There is no back data in raw bucket, please upload at least once!")


class S3Operator:
    """
    Class S3Operator.
    Use this class to manipulate data with S3 bucket.
    """

    def __init__(self) -> None:
        self.session = boto3.Session(
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_DEFAULT_REGION"),
        )
        self.s3 = self.session.resource("s3")

        self._prefix = ""
        self._bucket = None
        self.response = None

    """
        property
    """

    @property
    def bucket(self) -> str:
        return self._bucket

    @bucket.setter
    def bucket(self, bucket: str) -> None:
        print(f"☑️Setting bucket to {bucket}")
        self._bucket = bucket

    @property
    def prefix(self) -> str:
        return self._prefix

    @prefix.setter
    def prefix(self, path: str) -> None:
        print(f"☑️Setting prefix to {path}")
        self._prefix = path

    """
        method
    """

    def detect_prefix(self) -> Tuple[Dict, bool]:
        self.response = self.s3.meta.client.list_objects(
            Bucket=self._bucket, Prefix=self._prefix
        )
        if "Contents" in self.response:
            exist = True
        else:
            exist = False
        return exist

    def list_s3_obj(self) -> List:
        lst_obj_info = self.response.get("Contents", None)
        lst_file = [obj_info.get("Key", None) for obj_info in lst_obj_info]
        return lst_file

    def get_table_Dataframe(self, prefix: str, table: str, sep="|") -> pd.DataFrame:
        key = os.path.join(prefix, f"{table}.csv")
        response = self.s3.meta.client.get_object(Bucket=self.bucket, Key=key)
        df = pd.read_csv(response.get("Body"), sep=sep)
        return df

    def remove_object(
        self, table: str, prefix: None or str = None, bucket_name: None or str = None, extension : str = 'csv'
    ):
        if not bucket_name:
            bucket_name = self.bucket
        if not prefix:
            prefix = self.prefix

        key = os.path.join(prefix, f"{table}.{extension}")
        try:
            self.s3.meta.client.delete_object(Bucket=bucket_name, Key=key)
        except Exception as e:
            raise RuntimeError(f"Unexpected error removing object from S3: {e}")

    def table_exists(
        self, table: str, prefix: None or str = None, bucket_name: None or str = None, extension : str = 'csv'
    ) -> bool:
        if not bucket_name:
            bucket_name = self.bucket
        if not prefix:
            prefix = self.prefix

        key = os.path.join(prefix, f"{table}.{extension}")
        try:
            self.s3.Object(bucket_name=bucket_name, key=key).load()
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            else:
                # Something else has gone wrong.
                raise
        return True

    @decorator_manager.timeit(program_name="Download data from S3")
    def download_s3_obj(self, local_file_path: str, s3_file_path: str) -> None:
        if not os.path.isfile(local_file_path):
            self.s3.meta.client.download_file(
                self._bucket, s3_file_path, local_file_path
            )

    @decorator_manager.timeit(program_name="Send file to S3")
    def send_to_s3_file(self, local_file_path: str, s3_file_path: str) -> None:
        self.s3.meta.client.upload_file(
            Filename=local_file_path, Bucket=self._bucket, Key=s3_file_path
        )
        print(f"📑file is sent to {s3_file_path}.")

    def send_to_s3_obj(self, df: pd.DataFrame, s3_file_path: str, sep: str) -> None:
        """
        Converts a DataFrame (Pandas or Polars) to the appropriate format (Parquet or CSV)
        based on the file extension in the S3 path and uploads it to S3.

        Args:
            df (pandas.DataFrame or polars.DataFrame): The input DataFrame to be converted and uploaded.
            s3_file_path (str): The S3 path (including the file name) where the file should be uploaded.
            sep (str): The delimiter to use in the CSV file (if CSV is chosen). Default is ','.
        """
        
        # Determine file extension to select the correct format
        if s3_file_path.endswith('.parquet'):
            self.send_to_s3_parquet(df, s3_file_path)
        elif s3_file_path.endswith('.csv'):
            self.send_to_s3_csv(df, s3_file_path, sep)
        else:
            raise ValueError("S3 file path must end with either '.parquet' or '.csv'")

        # Print once the file is uploaded
        print(f"📤 File sent to {s3_file_path}.")

    @decorator_manager.timeit(program_name="Send df to S3 as Parquet")
    def send_to_s3_parquet(self, df, s3_file_path: str) -> None:
        """
        Converts a DataFrame (Pandas or Polars) to Parquet format and uploads it to S3.

        Args:
            df (pandas.DataFrame or polars.DataFrame): The input DataFrame to be converted and uploaded.
            s3_file_path (str): The S3 path (including the file name) where the Parquet file should be uploaded.
        """
        
        # Create a buffer to store the Parquet file
        parquet_buffer = io.BytesIO()

        # Check if the input is a Pandas DataFrame or a Polars DataFrame
        if isinstance(df, pd.DataFrame):
            # For pandas DataFrame, use pandas' to_parquet method
            df.to_parquet(parquet_buffer, index=False, compression='snappy')

        elif isinstance(df, pl.DataFrame):
            # For Polars DataFrame, use Polars' native write_parquet method
            df.write_parquet(parquet_buffer)

        else:
            raise ValueError("Input should be either a pandas or polars DataFrame")

        # Seek to the beginning of the buffer before uploading
        parquet_buffer.seek(0)

        # Upload the buffer to S3
        self.s3.meta.client.upload_fileobj(
            Fileobj=parquet_buffer, Bucket=self.bucket, Key=s3_file_path
        )
        
    @decorator_manager.timeit(program_name="Send df to S3 as CSV")
    def send_to_s3_csv(self, df, s3_file_path: str, sep: str = '|') -> None:
        """
        Converts a DataFrame (Pandas or Polars) to CSV format and uploads it to S3.

        Args:
            df (pandas.DataFrame or polars.DataFrame): The input DataFrame to be converted and uploaded.
            s3_file_path (str): The S3 path (including the file name) where the CSV file should be uploaded.
            sep (str): The delimiter to use in the CSV file. Default is ','.
        """
        
        # Create a buffer to store the CSV file
        csv_buffer = io.BytesIO()
        w = io.TextIOWrapper(csv_buffer, newline='')
        
        # Check if the input is a Pandas DataFrame or a Polars DataFrame
        if isinstance(df, pd.DataFrame):
            # For pandas DataFrame, use pandas' to_csv method
            df.to_csv(w, index=False, compression="gzip", sep=sep, quoting=csv.QUOTE_NONNUMERIC)

        elif isinstance(df, pl.DataFrame):
            # For Polars DataFrame, use Polars' to_pandas and then pandas' to_csv method
            df.to_pandas().to_csv(w, index=False, compression="gzip", sep=sep, quoting=csv.QUOTE_NONNUMERIC)
            
        else:
            raise ValueError("Input should be either a pandas or polars DataFrame")

        # Seek to the beginning of the buffer before uploading
        w.seek(0)

        # Upload the buffer to S3
        self.s3.meta.client.upload_fileobj(
            Fileobj=csv_buffer, Bucket=self.bucket, Key=s3_file_path
        )

    
    # def get_diff_file(self, local_folder_path):
    #     lst_obj = [obj for obj in os.listdir(local_folder_path) if not obj.startswith(".")]
    #     lst_local_file = [obj for obj in lst_obj if os.path.isfile(os.path.join(local_folder_path, obj))]
    #     if len(lst_obj) != len(lst_local_file):
    #         raise TypeError(f"⚠️{set(lst_obj) - set(lst_local_file)} are not files!")
