#!/usr/bin/env python3
"""0. Regex-ing """
import logging
import re


def filter_datum(fields: list, redaction: str, message: str,
                 separator: str) -> str:
    """Function that filters a string to redact specified fields"""
    for field in fields:
        replace = re.compile(rf'{re.escape(field)}=[^{separator}]*')
        message = replace.sub(f'{field}={redaction}', message)
        logging.debug("After redacting '{}': {}".format(field, message))
    return message
