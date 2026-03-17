import logging
import os
from datetime import datetime


class Logger:

    def __init__(self, log_file="scan.log"):

        self.log_file = log_file

        self.logger = logging.getLogger("MiniWebScanner")

        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:

            file_handler = logging.FileHandler(self.log_file)

            console_handler = logging.StreamHandler()

            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )

            file_handler.setFormatter(formatter)

            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

            self.logger.addHandler(console_handler)

    def info(self, message):

        self.logger.info(message)

    def warning(self, message):

        self.logger.warning(message)

    def error(self, message):

        self.logger.error(message)

    def debug(self, message):

        self.logger.debug(message)