from __future__ import annotations

import argparse
from typing import Any, Optional

from .._compat import Final
from ..core import Line, Rule
from ..utils.colorful import BACK_RED, RED, RST, Color

TAB: Final[str] = "\t"


class ReplaceTabWithSpaceRule(Rule):
    """
    The rule to insert a whitespece between Chinese and English characters.
    """

    rule_name: str = "ReplaceTabWithSpace"
    rule_type: set[str] = {"line"}
    hint_color: Color = RED

    indent_size: int
    options = {}

    def __init__(self, cli: argparse.Namespace) -> None:
        super().__init__(cli)
        self.enable = self.options["enable"]
        self.indent_size = self.options["indent_size"]

    @classmethod
    def extend_cli(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--replace-tab-with-space",
            action="store_true",
        )
        parser.add_argument(
            "--replace-tab-with-space-indent-size",
            type=int,
            default=4,
        )

    def extract_options_from_cli(self, cli: argparse.Namespace) -> dict[str, Any]:
        return {
            "enable": cli.replace_tab_with_space or cli.all_rules,
            "indent_size": cli.replace_tab_with_space_indent_size,
        }

    def format_line(self, line: Line) -> None:
        line.text = format(line.text, self.indent_size)

    def check_line(self, line: Line) -> Optional[tuple[str, int]]:
        text = line.text

        if TAB not in text:
            return None

        self.count += 1
        return highlight(text, self.indent_size, self.hint_max_len)


def format(text: str, indent_size: int) -> str:
    while (pos := text.find(TAB)) != -1:
        text = text[:pos] + " " * (indent_size - pos % indent_size) + text[pos + 1 :]
    return text


def highlight(text: str, indent_size: int, hint_max_len: int) -> tuple[str, int]:
    start = text.find(TAB)
    while (pos := text.find(TAB)) != -1:
        text = text[:pos] + BACK_RED + " " * (indent_size - pos % indent_size) + RST + text[pos + 1 :]

    start = max(0, start - 10)
    end = min(len(text), start + hint_max_len)
    text = text[start:end]
    return text, start
