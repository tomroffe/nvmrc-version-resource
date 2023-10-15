from os import environ

from unittest import TestCase
from logging import Logger
from nvmrc_version.logs import log


class LoggingUnittests(TestCase):
    def test_logging(self):
        logging = log
        assert isinstance(logging, Logger)

    def test_logger_is_rich_handler(self):
        logging = log.name
        assert logging == "rich"
