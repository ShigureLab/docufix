from __future__ import annotations

import argparse
from typing import Any, Optional

from ..core import File, Rule
from ..utils.colorful import CYAN, Color
from ..utils.newline import Newline, NewlineName


class UnifyNewlineRule(Rule):
    """
    The rule to insert a whitespece between Chinese and English characters.
    """

    rule_name: str = "UnifyNewline"
    rule_type: set[str] = {"file"}
    hint_color: Color = CYAN

    options = {}
    newline: Newline = Newline.LF

    def __init__(self, cli: argparse.Namespace) -> None:
        super().__init__(cli)
        self.enable = self.options["enable"]
        newline_name: NewlineName = self.options["newline"]
        self.newline = Newline.from_name(newline_name)

    @classmethod
    def extend_cli(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--unify-newline",
            action="store_true",
        )
        parser.add_argument(
            "--unify-newline-type",
            choices=["CR", "LF", "CRLF"],
            type=str.upper,
            default="LF",
        )

    def extract_options_from_cli(self, cli: argparse.Namespace) -> dict[str, Any]:
        return {
            "enable": cli.unify_newline or cli.all_rules,
            "newline": cli.unify_newline_type,
        }

    def format_file(self, file: File) -> None:
        for line in file.lines:
            line.change_newline(self.newline)

    def check_file(self, file: File) -> Optional[str]:
        for line in file.lines:
            if self.newline == Newline.LF and line.newline == Newline.CRLF:
                self.count += 1
                return "Expected LF newline, but found CRLF"
            elif self.newline == Newline.CRLF and line.newline == Newline.LF:
                self.count += 1
                return "Expected CRLF newline, but found LF"
        return None
