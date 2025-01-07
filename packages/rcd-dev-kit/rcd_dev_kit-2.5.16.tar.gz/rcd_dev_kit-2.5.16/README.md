# rcd_dev_kit
### Developed by Real Consulting Data

## Description
We've developed `rcd-dev-kit` to facilitate the manipulation and interaction with the OIP ecosystem.


## Installation
```bash
pip install rcd-dev-kit
```

## Modules
We've divided our functions in four main modules:
- [database_manager](./src/rcd_dev_kit/database_manager)
    - Classes:
        - [GcloudOperator()](./src/rcd_dev_kit/database_manager/gcloud_operator.py)
        - MysqlOperator()
        - ElasticsearchOperator()
        - RedshiftOperator()
        - SnowflakeOperator()
        - S3Operator()
    - Main Functions:
        - index_json_bulk()
        - index_json()
        - index_json_bulk_parallel()
        - [send_to_redshift()](./src/rcd_dev_kit/database_manager/redshift_operator.py)
        - read_from_redshift()
        - [send_metadata_to_redshift()](./src/rcd_dev_kit/database_manager/redshift_operator.py)
        - find_tables_by_column_name()
        - migrate_metadata_from_redshift()
        - upload_raw_s3()
        - download_raw_s3()
        - [upload_to_gcloud()](./src/rcd_dev_kit/database_manager/gcloud_operator.py)
        - [download_from_gcloud()](./src/rcd_dev_kit/database_manager/gcloud_operator.py)

- [dataclass_manager](./src/rcd_dev_kit/dataclass_manager)
    - Classes:
        - RawDataFile()

- [decorator_manager](./src/rcd_dev_kit/decorator_manager)
    - Main Functions:
        - timeit()
        - debug()

- [file_manager](./src/rcd_dev_kit/file_manager)
    - Classes:
        - FileOperator()
        - [FileDownloader()](./src/rcd_dev_kit/file_manager/file_downloader.py)
    - Main Functions:
        - detect_path()
        - detect_all_files()
        - write_df_to_json_parallel()
        - download_excel()
        - download_csv()
        - download_pdf()
        - download_zip()

- [pandas_manager](./src/rcd_dev_kit/pandas_manager)
    - Main Functions:
        - strip_all_text_column()
        - check_na()
        - check_duplication()
        - check_quality_table_names()
        - normalize_date_column()
        - detect_aws_type()

- [sql_utils](./src/rcd_dev_kit/sql_utils)
    - Main Functions:
        - convert_to_snowflake_syntax()
        - correct_sql_system_variables_syntax()

## Pre-requirements
Since some of the functions deal with database connections(S3, Redshift, Snowflake, GCP, Elasticsearch, ...), we must
be careful to sensitive information. Thus, to use the functions correctly we must have a `.env` file following
the `.env.example` template.

## Feedback
Any questions or suggestions?
Please contact package maintainer.

# python-sdk
Refer to book https://py-pkgs.org/01-introduction for best practices

# Maintainers
This package is using poetry for pkg management, it must be installed locally if you are maintaining the package.  
For developing and test the pkg locally, you must run `poetry install`.

**This git repository has an automated CI/CD process** found on the git worflow: [main.yml](.github/workflows/main.yml). It means that once all modifications have been made, a Pull Request to main will trigger a serie of actions:    
- Install Package: `poetry install`
- Run Unitary Tests: `poetry run pytest -v tests/ --cov=rcd_dev_kit --cov-report=xml`
- Build Package: `poetry build`
- Publish Package in PyPI: `poetry publish`
- Install Package from PyPI: `pip install rcd_dev_kit`
- Send a Teams message with the new available version: Git Image `toko-bifrost/ms-teams-deploy-card@master`.

## Contributing
Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License
`rcd_dev_kit` was created by RCD. It is licensed under the terms of the MIT license.

## Credits
`rcd_dev_kit` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).


## [![Repography logo](https://images.repography.com/logo.svg)](https://repography.com) / Top contributors
[![Top contributors](https://images.repography.com/38594109/daviibf/rcd-dev-kit/top-contributors/HnXXnUSGHxL47D8CGGmXE5g5nBhf2-iL3DAPxGcfUQg/6SSkjzuhw9SDmQVgkklseoZkiLprWCMi_Pcey2Qyx1g_table.svg)](https://github.com/daviibf/rcd-dev-kit/graphs/contributors)

## [![Repography logo](https://images.repography.com/logo.svg)](https://repography.com) / Recent activity [![Time period](https://images.repography.com/38594109/daviibf/rcd-dev-kit/recent-activity/HnXXnUSGHxL47D8CGGmXE5g5nBhf2-iL3DAPxGcfUQg/6SSkjzuhw9SDmQVgkklseoZkiLprWCMi_Pcey2Qyx1g_badge.svg)](https://repography.com)
[![Timeline graph](https://images.repography.com/38594109/daviibf/rcd-dev-kit/recent-activity/HnXXnUSGHxL47D8CGGmXE5g5nBhf2-iL3DAPxGcfUQg/6SSkjzuhw9SDmQVgkklseoZkiLprWCMi_Pcey2Qyx1g_timeline.svg)](https://github.com/daviibf/rcd-dev-kit/commits)
[![Trending topics](https://images.repography.com/38594109/daviibf/rcd-dev-kit/recent-activity/HnXXnUSGHxL47D8CGGmXE5g5nBhf2-iL3DAPxGcfUQg/6SSkjzuhw9SDmQVgkklseoZkiLprWCMi_Pcey2Qyx1g_words.svg)](https://github.com/daviibf/rcd-dev-kit/commits)
[![Top contributors](https://images.repography.com/38594109/daviibf/rcd-dev-kit/recent-activity/HnXXnUSGHxL47D8CGGmXE5g5nBhf2-iL3DAPxGcfUQg/6SSkjzuhw9SDmQVgkklseoZkiLprWCMi_Pcey2Qyx1g_users.svg)](https://github.com/daviibf/rcd-dev-kit/graphs/contributors)
[![Activity map](https://images.repography.com/38594109/daviibf/rcd-dev-kit/recent-activity/HnXXnUSGHxL47D8CGGmXE5g5nBhf2-iL3DAPxGcfUQg/6SSkjzuhw9SDmQVgkklseoZkiLprWCMi_Pcey2Qyx1g_map.svg)](https://github.com/daviibf/rcd-dev-kit/commits)
