from __future__ import annotations


class LineTrimer:

    newline: str

    def __init__(self, newline: str):
        self.newline = newline

    @classmethod
    def create(cls, line: str) -> tuple["LineTrimer", str]:
        if line.endswith("\r\n"):
            newline = "\r\n"
        elif line.endswith("\n"):
            newline = "\n"
        else:
            newline = ""

        self = cls(newline)
        return self, self.trim(line)

    def trim(self, line: str) -> str:
        return line.rstrip(self.newline)

    def restore(self, line: str, force_lf: bool = False) -> str:
        newline = self.newline
        if force_lf and self.newline:
            newline = "\n"
        return line + newline
