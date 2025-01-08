import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class Tupan:
    @staticmethod
    def get_input(key):
        """
        Get input data from the environment variable
        :param key: key to get from the input data
        :return: value of the key
        """
        try:
            input_data = json.loads(os.getenv('INPUT', '{}'))
            return input_data.get(key, None)
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error parsing input data: {e}")
            return None

    @staticmethod
    def set_output(value):
        """
        Set output data
        :param value: value to set as output
        :return: None
        """
        try:
            logger.info(f"::output::{json.dumps(value)}")
        except (TypeError, ValueError) as e:
            logger.error(f"Error setting output data: {e}")

    @staticmethod
    def set_next_job(job):
        """
        Set the next job to run
        :param job_name: name of the next job to run
        :return: None
        """
        try:
            logger.info(f"::next-job::{json.dumps(job)}")
        except (TypeError, ValueError) as e:
            logger.error(f"Error setting next job: {e}")
