from __future__ import annotations

import argparse
from typing import Any, Optional

from ..core import File, Rule
from ..utils.colorful import YELLOW, Color
from ..utils.newline import Newline


class EnsureFinalNewlineRule(Rule):
    """
    The rule to insert a whitespece between Chinese and English characters.
    """

    rule_name: str = "EnsureFinalNewline"
    rule_type: set[str] = {"file"}
    hint_color: Color = YELLOW

    options = {}

    def __init__(self, cli: argparse.Namespace) -> None:
        super().__init__(cli)
        self.enable = self.options["enable"]

    @classmethod
    def extend_cli(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--ensure-final-newline",
            action="store_true",
        )

    def extract_options_from_cli(self, cli: argparse.Namespace) -> dict[str, Any]:
        return {
            "enable": cli.ensure_final_newline or cli.all_rules,
        }

    def _infer_newline(self, file: File) -> Newline:
        if file.lines:
            if file.lines[0].newline is not None:
                return file.lines[0].newline
        return Newline.LF

    def format_file(self, file: File) -> None:
        newline = self._infer_newline(file)

        if file.lines and file.lines[-1].newline is None:
            file.lines[-1].newline = newline

    def check_file(self, file: File) -> Optional[str]:
        if file.lines and file.lines[-1].newline is None:
            self.count += 1
            return "Missing final newline"
        return None
