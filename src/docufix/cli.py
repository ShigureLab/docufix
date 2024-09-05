from __future__ import annotations

import argparse

from .core import Rule


def setup_cli() -> argparse.ArgumentParser:
    """Setup the CLI parser and basic arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("globs", help="Path glob to check", nargs="+")
    parser.add_argument("--fix", help="Auto fix the wrongs", action="store_true")
    parser.add_argument("--ignore-globs", help="Path glob to ignore, comma separated", type=str, default="")
    parser.add_argument("--all-rules", action="store_true", help="Apply all existing rules")
    return parser


def setup_cli_for_test() -> argparse.ArgumentParser:
    """Setup the CLI parser with some options must specific."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-rules", action="store_true", help="Apply all existing rules")
    return parser


def cli(rule_clss: list[type[Rule]]) -> argparse.Namespace:
    parser = setup_cli()
    for rule_cls in rule_clss:
        rule_cls.extend_cli(parser)
    args = parser.parse_args()
    return args
