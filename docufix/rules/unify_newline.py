from __future__ import annotations

import argparse
from typing import Any, Literal, Optional

from ..core import File, Rule
from ..utils.colorful import CYAN, Color


class UnifyNewlineRule(Rule):
    """
    The rule to insert a whitespece between Chinese and English characters.
    """

    rule_name: str = "UnifyNewline"
    rule_type: set[str] = {"file"}
    hint_color: Color = CYAN

    options = {}
    newline: Literal["lf", "crlf"] = "lf"

    def __init__(self, cli: argparse.Namespace) -> None:
        super().__init__(cli)
        self.enable = self.options["enable"]
        self.newline = self.options["newline"]

    @classmethod
    def extend_cli(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--unify-newline",
            action="store_true",
        )
        parser.add_argument(
            "--unify-newline-type",
            choices=["lf", "crlf"],
            default="lf",
        )

    def extract_options_from_cli(self, cli: argparse.Namespace) -> dict[str, Any]:
        return {
            "enable": cli.unify_newline,
            "newline": cli.unify_newline_type,
        }

    def format_file(self, file: File) -> None:
        for line in file.lines:
            if self.newline == "lf":
                line.force_lf()
            else:
                line.force_crlf()

    def lint_file(self, file: File) -> Optional[str]:
        for line in file.lines:
            if line.newline == "\r\n" and self.newline == "lf":
                return "Expected LF newline, but found CRLF"
            elif line.newline == "\n" and self.newline == "crlf":
                return "Expected CRLF newline, but found LF"
        return None
