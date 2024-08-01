#!/usr/bin/env python3
""" Module that contains a filter_datum function """

import re
import os
from typing import List
import logging
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns the log message obfuscated """
    for field in fields:
        message = re.sub(rf'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Constructor method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Method that returns the log message obfuscated """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """ Method that returns a logger object """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Returns a connector to the database """
    host = os.getenv('PERSONAL_DATA_DB_HOST') or 'localhost'
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or 'root'
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ''
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=database
    )

def main() -> None:
    """ Main function"""
    logger = get_logger()

    connector = get_db()
    cursor = connector.cursor()

    cursor.execute('SELECT * FROM `users`;')
    users = cursor.fetchall()

    column_names = cursor.column_names

    for user in users:
        formatted_user = "".join(f"{attribute}={value}; " for
                                 attribute, value in zip(column_names, user))
        logger.info(formatted_user)


if __name__ == '__main__':
    main()
