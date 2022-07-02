import argparse
from typing import Any, Optional

from ..utils.colorful import CYAN, RST, Color


class BaseRule:
    """
    The base class of the rule.

    Args:
        cli (argparse.Namespace): The command line arguments.
    """

    rule_name: str = "BaseRule"
    rule_type: set[str] = {"line", "file"}
    hint_color: Color = CYAN

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

    def format_line(self, line: str) -> str:
        """
        This function is used to format the line.

        Args:
            line (str): The line content.

        Returns:
            str: The formatted line content.
        """
        return ""

    def lint_line(self, line: str) -> Optional[tuple[str, int]]:
        """
        This function is used to lint the line. The lint message seems like:

        .. text-block:: text

            {rule_name}\t{filepath}:{lineno}:{colno}\t\t{highlight_string}

        Args:
            line (str): The line to lint.

        Returns:
            Optional[tuple[str, int]]: The highlight string and the column number.
                If this line needn't to be highlighted, return None.
        """
        return None

    def format_file(self, file_str: str) -> str:
        """
        This function is used to format the file.

        Args:
            file_str (str): The file content.

        Returns:
            str: The formatted file content.
        """
        return ""

    def lint_file(self, file_str: str) -> bool:
        """
        This function is used to lint the file. The lint message seems like:

        .. text-block:: text

            {rule_name}\t{filepath}

        Args:
            file_str (str): The file to lint.

        Returns:
            bool: If this file needn't to be linted, return False.
        """
        return False

    @property
    def colored_rule_name(self) -> str:
        """
        The colored rule name.
        """
        return f"{self.hint_color}{self.rule_name}{RST}"
