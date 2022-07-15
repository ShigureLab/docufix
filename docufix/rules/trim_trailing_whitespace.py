from __future__ import annotations

import argparse
import re
from typing import Any, Optional

from ..core import Line, Rule
from ..utils.colorful import BACK_MAGENTA, MAGENTA, RST, Color

REGEX_TRILING_WHITESPACE = re.compile(r"(?P<spaces>\s+)$")


class TrimTrailingWhitespace(Rule):
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
            "enable": cli.trim_trailing_whitespace or cli.all_rules,
        }

    def format_line(self, line: Line) -> None:
        line.text = format(line.text)

    def check_line(self, line: Line) -> Optional[tuple[str, int]]:
        text = line.text
        if mth := REGEX_TRILING_WHITESPACE.search(text):
            self.count += 1
            start, end = mth.span()
        else:
            return None

        start = max(0, start - 10)
        end = min(len(text), end + 10, start + self.hint_max_len)

        text = text[start:end]
        text = REGEX_TRILING_WHITESPACE.sub(rf"{BACK_MAGENTA}\g<spaces>{RST}", text)
        return text, start


def format(text: str) -> str:
    text = REGEX_TRILING_WHITESPACE.sub("", text)
    return text
