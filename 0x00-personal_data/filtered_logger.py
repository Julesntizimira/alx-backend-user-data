#!/usr/bin/env python3
'''Regex-ing
   module
'''
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    '''returns the log
       message obfuscated
    '''
    msgs = message.split(separator)
    msglist = []
    for msg in msgs:
        msg_fiels = msg.split("=")
        if msg_fiels[0] in fields:
            pattern = r'=(.*)'
            replacement = rf'={redaction}'
            new_msg = re.sub(pattern, replacement, msg)
            msglist.append(new_msg)
        else:
            msglist.append(msg)
    result = ""
    for msg in msglist:
        result = result + msg + separator
    return result
