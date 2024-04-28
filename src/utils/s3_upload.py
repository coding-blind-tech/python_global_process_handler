import boto3
import logging
import math
import os
import tempfile
from shutil import make_archive
from botocore.config import Config
from boto3.s3.transfer import TransferConfig

logger = logging.getLogger(f'app.{__name__}')


def upload_logs(region, s3_bucket):
    """ Upload logs to S3 """
    logger.info('Starting log archive upload to S3.')
    logger.debug(f'the S3 bucket name is : -> {s3_bucket}')
    if region.startswith('us-gov'):
        _resource = boto3.resource(
            's3', region_name=region, endpoint_url='https://s3-fips.{}.amazonaws.com'.format(region))
    else:
        _resource = boto3.resource('s3', region_name=region)

    # Grab logs from temp directory
    log_dir = os.path.join(tempfile.gettempdir(), 'logs')
    # Create a zip archive of the logs
    make_archive('app_logging_archive', 'zip', log_dir)
    # Configure Multipart Upload for Optimal Upload Speed
    file_size = os.path.getsize("app_logging_archive.zip")
    num_cpus = os.cpu_count()
    transfer_config = TransferConfig(
        multipart_threshold=1024 * 10,
        max_concurrency=num_cpus,
        multipart_chunksize=math.floor(file_size / num_cpus),
        use_threads=True)
    # Upload Object using TransferConfig
    _resource.Object(
        bucket_name=s3_bucket,
        key="kblackwelder_test/app_logging_archive.zip"
    ).upload_file(
        Filename="app_logging_archive.zip",
        Config=transfer_config
    )
    logger.info('Finished uploading log archive to S3.')
