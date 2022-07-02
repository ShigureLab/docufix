from __future__ import annotations

import argparse
import re
from typing import Any, Optional

from ..utils.colorful import RST, Color, BACK_MAGENTA, MAGENTA
from ._abc import BaseRule

REGEX_TRILING_WHITESPACE = re.compile(r"(?P<spaces>\s+)$")


class TrimTrailingWhitespace(BaseRule):
    """
    The rule to insert a whitespece between Chinese and English characters.
    """

    rule_name: str = "TrimTrailingWhitespace"
    rule_type: set[str] = {"line"}
    hint_color: Color = MAGENTA

    options = {}

    def __init__(self, cli: argparse.Namespace) -> None:
        super().__init__(cli)
        self.enable = self.options["enable"]

    @classmethod
    def extend_cli(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--trim-trailing-whitespace",
            action="store_true",
        )

    def extract_options_from_cli(self, cli: argparse.Namespace) -> dict[str, Any]:
        return {
            "enable": cli.trim_trailing_whitespace,
        }

    def format_line(self, line: str) -> str:
        with_newline = line.endswith("\n")
        if with_newline:
            line.rstrip("\n")
        line = REGEX_TRILING_WHITESPACE.sub("", line)
        if with_newline:
            line += "\n"
        return line

    def lint_line(self, line: str) -> Optional[tuple[str, int]]:
        line = line.rstrip("\n")
        if mth := REGEX_TRILING_WHITESPACE.search(line):
            self.count += 1
            start, end = mth.span()
        else:
            return None

        start = max(0, start - 10)
        end = min(len(line), end + 10, start + self.hint_max_len)

        line = line[start:end]
        line = REGEX_TRILING_WHITESPACE.sub(rf"{BACK_MAGENTA}\g<spaces>{RST}", line)
        return line, start
