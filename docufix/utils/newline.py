from __future__ import annotations

from enum import Enum
from typing import Literal

NewlineName = Literal["CR", "LF", "CRLF"]
NewlineValue = Literal["\r", "\n", "\r\n"]


class Newline(Enum):
    CR = "\r"
    LF = "\n"
    CRLF = "\r\n"

    @classmethod
    def from_name(cls, name: NewlineName) -> "Newline":
        if name == "CR":
            return cls.CR
        elif name == "LF":
            return cls.LF
        elif name == "CRLF":
            return cls.CRLF

    @classmethod
    def values(cls) -> list[NewlineValue]:
        return [item.value for item in cls]
