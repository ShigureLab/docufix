from __future__ import annotations

import argparse
import re
from typing import Any, Optional

from ..core import Line, Rule
from ..utils.colorful import BLUE, RST, Color

REGEX_CN_CHAR_STR = r"[\u4e00-\u9fa5]"
REGEX_EN_CHAR_STR = r"[a-zA-Z0-9]"

REGEX_CN_WITH_EN = re.compile(f"(?P<cn>{REGEX_CN_CHAR_STR})(?P<en>{REGEX_EN_CHAR_STR})")
REGEX_EN_WITH_CN = re.compile(f"(?P<en>{REGEX_EN_CHAR_STR})(?P<cn>{REGEX_CN_CHAR_STR})")


class InsertWhitespaceBetweenCnAndEnCharRule(Rule):
    """
    The rule to insert a whitespece between Chinese and English characters.
    """

    rule_name: str = "InsertWhitespaceBetweenCnAndEnChar"
    rule_type: set[str] = {"line"}
    hint_color: Color = BLUE

    options = {}

    def __init__(self, cli: argparse.Namespace) -> None:
        super().__init__(cli)
        self.enable = self.options["enable"]

    @classmethod
    def extend_cli(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--insert-whitespace-between-cn-and-en-char",
            action="store_true",
        )

    def extract_options_from_cli(self, cli: argparse.Namespace) -> dict[str, Any]:
        return {
            "enable": cli.insert_whitespace_between_cn_and_en_char or cli.all_rules,
        }

    def format_line(self, line: Line):
        line.text = format(line.text)

    def check_line(self, line: Line) -> Optional[tuple[str, int]]:
        text = line.text
        min_start = 999999
        max_end = -1
        found = False
        for mth in REGEX_CN_WITH_EN.finditer(text):
            self.count += 1
            found = True
            start, end = mth.span()
            min_start = min(min_start, start)
            max_end = max(max_end, end)
        for mth in REGEX_EN_WITH_CN.finditer(text):
            self.count += 1
            found = True
            start, end = mth.span()
            min_start = min(min_start, start)
            max_end = max(max_end, end)

        if not found:
            return None

        start = max(0, min_start - 10)
        end = min(len(text), max_end + 10, start + self.hint_max_len)

        text = text[start:end]
        text = REGEX_EN_WITH_CN.sub(rf"{self.hint_color}\g<en>\g<cn>{RST}", text)
        text = REGEX_CN_WITH_EN.sub(rf"{self.hint_color}\g<cn>\g<en>{RST}", text)
        return text, min_start


def format(text: str) -> str:
    text = REGEX_CN_WITH_EN.sub(r"\g<cn> \g<en>", text)
    text = REGEX_EN_WITH_CN.sub(r"\g<en> \g<cn>", text)
    return text
