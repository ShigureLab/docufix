from __future__ import annotations

import argparse
from typing import Any, Optional

from .utils.colorful import CYAN, RST, Color
from .utils.newline import Newline


class Rule:
    """
    The base class of the rule.

    Args:
        cli (argparse.Namespace): The command line arguments.
    """

    rule_name: str = "BaseRule"
    rule_type: set[str] = {"line", "file"}
    hint_color: Color = CYAN
    hint_max_len = 40

    enable: bool
    options: dict[str, Any]

    def __init__(self, cli: argparse.Namespace) -> None:
        self.options = self.extract_options_from_cli(cli)
        self.count = 0

    def extract_options_from_cli(self, cli: argparse.Namespace) -> dict[str, Any]:
        return {}

    @classmethod
    def extend_cli(cls, parser: argparse.ArgumentParser) -> None:
        return

    def format_line(self, line: "Line") -> None:
        """
        This function is used to format the line.

        Args:
            line (str): The line content.

        Returns:
            str: The formatted line content.
        """
        return

    def check_line(self, line: "Line") -> Optional[tuple[str, int]]:
        """
        This function is used to check the line. The check message seems like:

        .. text-block:: text

            {rule_name}\t{filepath}:{lineno}:{colno}\t\t{highlight_string}

        Args:
            line (str): The line to check.

        Returns:
            Optional[tuple[str, int]]: The highlight string and the column number.
                If this line needn't to be highlighted, return None.
        """
        return None

    def format_file(self, file: "File") -> None:
        """
        This function is used to format the file.

        Args:
            file_str (str): The file content.

        Returns:
            str: The formatted file content.
        """
        return

    def check_file(self, file: "File") -> Optional[str]:
        """
        This function is used to check the file. The check message seems like:

        .. text-block:: text

            {rule_name}\t{filepath}

        Args:
            file_str (str): The file to check.

        Returns:
            bool: If this file needn't to be checked, return False.
        """
        return None

    @property
    def colored_rule_name(self) -> str:
        """
        The colored rule name.
        """
        return f"{self.hint_color}{self.rule_name}{RST}"

    @property
    def is_line_rule(self) -> bool:
        return "line" in self.rule_type

    @property
    def is_file_rule(self) -> bool:
        return "file" in self.rule_type


class Line:
    text: str
    newline: Optional[Newline]

    def __init__(self, lineno: int, text: str, file: "File"):
        self.lineno = lineno
        self.origin_text = text
        self.file = file

        self.text, self.newline = self._process_origin_text(self.origin_text)
        self._check_line()

    def _process_origin_text(self, origin_text: str) -> tuple[str, Optional[Newline]]:

        if origin_text.endswith(Newline.CRLF.value):
            newline = Newline.CRLF
        elif origin_text.endswith(Newline.CR.value):
            newline = Newline.CR
        elif origin_text.endswith(Newline.LF.value):
            newline = Newline.LF
        else:
            newline = None

        text = origin_text
        if newline is not None:
            text = origin_text.rstrip(newline.value)

        return text, newline

    def _check_line(self) -> None:
        assert not self.text.endswith(tuple(Newline.values())), "The trimed text should not end with newline."
        assert self.text or self.newline, "The line should not be empty."

    def change_newline(self, newline: Newline) -> None:
        if self.newline is not None:
            self.newline = newline

    def apply_rules(self, rules: list[Rule]):
        for rule in rules:
            if rule.is_line_rule:
                if (check_result := rule.check_line(self)) is not None:
                    highlight_string, colno = check_result
                    print(f"{rule.colored_rule_name}\t{self.file.filepath}:{self.lineno}:{colno}\t\t{highlight_string}")
                rule.format_line(self)

    @property
    def text_only(self) -> bool:
        return self.newline is None

    @property
    def newline_only(self) -> bool:
        return self.text == ""

    def __str__(self) -> str:
        if self.newline is not None:
            return self.text + self.newline.value
        else:
            return self.text


class File:

    filepath: str
    lines: list["Line"]

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.lines = self.read_lines()

    def read_lines(self) -> list["Line"]:
        lines: list["Line"] = []
        with open(self.filepath, "r", encoding="utf-8", newline="\n") as f:
            for lineno, line in enumerate(f, 1):
                lines.append(Line(lineno, line, self))
        return lines

    def apply_rules(self, rules: list[Rule]):
        for line in self.lines:
            line.apply_rules(rules)

        for rule in rules:
            if rule.is_file_rule:
                if rule.check_file(self):
                    print(f"{rule.colored_rule_name}\t{self.filepath}")
                rule.format_file(self)

    @property
    def text(self) -> str:
        return "".join(str(line) for line in self.lines)

    def write_back(self):
        with open(self.filepath, "w", encoding="utf-8", newline="\n") as f:
            f.write(self.text)
