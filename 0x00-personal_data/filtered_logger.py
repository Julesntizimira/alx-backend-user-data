#!/usr/bin/env python3
'''Personal data tasks
'''
import re
from typing import List
import logging
import sys


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''returns the log
       message obfuscated
    '''
    for field in fields:
        pattern = re.compile(fr'{re.escape(field)}=.*?{re.escape(separator)}')
        replacement = f'{field}={redaction}{separator}'
        message = re.sub(pattern, replacement, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """init constructor method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Log formatter recods"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    '''return a Logger'''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate(False)
    stdout = logging.StreamHandler(stream=sys.stdout)
    stdout.setLevel(logging.INFO)
    fmt = RedactingFormatter(PII_FIELDS)
    stdout.setFormatter(fmt)
    logger.StreamHandler(stdout)
    return logger
