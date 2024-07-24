"""TODO - doc it.
"""
from enum import Enum


class TestStatus(Enum):
    PASS = ("PASS", "GREEN",  False)
    FAIL = ("FAIL", "RED",    True)
    ERR = ("ERR",  "YELLOW", False)
    INIT = ("INIT", "BLEU",   True)

    def __init__(self, code: str, color: str, trunc_reason: bool):
        self.code = code
        self.color = color
        self.reason: str = ""
        self.trunc_reason = trunc_reason
