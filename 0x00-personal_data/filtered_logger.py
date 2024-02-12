#!/usr/bin/env python3
'''Personal data tasks
'''
import re
from typing import List
import logging
import os
from mysql.connector import connection


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
    user_data = logging.getLogger("user_data")
    user_data.setLevel(logging.INFO)
    user_data.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    user_data.addHandler(stream_handler)
    return user_data


def get_db() -> connection.MySQLConnection:
    '''return a connector'''
    return connection.MySQLConnection(
        host=os.getenv("PERSONAL_DATA_DB_HOST"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )


def main() -> None:
    '''main func'''
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    for row in rows:
        row_str = ";".join([f"{col}={val}" for col, val in zip(cursor.column_names, row)])
        log_record = logging.LogRecord("my_logger", logging.INFO, None, None, row_str, None, None)
        print(formatter.format(log_record))
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()