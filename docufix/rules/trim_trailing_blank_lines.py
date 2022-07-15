from __future__ import annotations

import argparse
from typing import Any, Optional

from ..core import File, Rule
from ..utils.colorful import GREEN, Color


class TrimTrailingBlankLinesRule(Rule):
    """
    The rule to insert a whitespece between Chinese and English characters.
    """

    rule_name: str = "TrimTrailingBlankLines"
    rule_type: set[str] = {"file"}
    hint_color: Color = GREEN

    options = {}

    def __init__(self, cli: argparse.Namespace) -> None:
        super().__init__(cli)
        self.enable = self.options["enable"]

    @classmethod
    def extend_cli(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--trim-trailing-blank-lines",
            action="store_true",
        )

    def extract_options_from_cli(self, cli: argparse.Namespace) -> dict[str, Any]:
        return {
            "enable": cli.trim_trailing_blank_lines or cli.all_rules,
        }

    def format_file(self, file: File) -> None:
        if not file.lines:
            return

        repeated_newline_count = 0

        for line in reversed(file.lines):
            if line.newline_only:
                repeated_newline_count += 1
            else:
                break

        if not repeated_newline_count:
            return

        file.lines = file.lines[:-repeated_newline_count]

    def check_file(self, file: File) -> Optional[str]:
        if file.lines and file.lines[-1].newline_only:
            self.count += 1
            return "The file has a repeated final newline."
        return None
