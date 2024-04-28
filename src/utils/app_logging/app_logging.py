import json
import tempfile
import os
import logging
from logging import config

# Get the temporary directory
temp_dir = tempfile.gettempdir()


def logging_setup():
    """
    Configure logging
    :return: None
    """

    # Open config file and load it
    logging_config_path = os.path.join(
        os.path.dirname(__file__), 'logging.config.json')
    with open(logging_config_path, 'r') as logging_config_file:
        logging_config = json.load(logging_config_file)

    # create the log dir
    log_dir = os.path.join(temp_dir, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Set the file handler filename
    logging_config['handlers']['file_handler']['filename'] = os.path.join(
        log_dir, 'app_app.log')

    # Configure logging
    config.dictConfig(logging_config)

    # create a logger and info out confirmation
    logger = logging.getLogger(f'app.{__name__}')
    logger.info('Logging configured')
