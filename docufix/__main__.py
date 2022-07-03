import argparse
import glob

from .core import File, Rule
from .rules import (
    InsertWhitespaceBetweenCnAndEnCharRule,
    TrimTrailingWhitespace,
    UnifyNewlineRule,
    EnsureFinalNewlineRule,
    TrimTrailingBlankLinesRule,
)


def main() -> None:
    rule_clss = [
        InsertWhitespaceBetweenCnAndEnCharRule,
        TrimTrailingWhitespace,
        UnifyNewlineRule,
        EnsureFinalNewlineRule,
        TrimTrailingBlankLinesRule,
    ]

    parser = argparse.ArgumentParser()
    parser.add_argument("glob", help="Path glob to check")
    parser.add_argument("--fix", help="Auto fix the wrongs", action="store_true")
    for rule_cls in rule_clss:
        rule_cls.extend_cli(parser)
    args = parser.parse_args()

    rules: list[Rule] = [rule_cls(args) for rule_cls in rule_clss]
    rules = [rule for rule in rules if rule.enable]

    # Show the enabled rules.
    if rules:
        print("Enabled rules:")
        for rule in rules:
            print(f"    {rule.colored_rule_name}\tType: {rule.rule_type}")
        print()
    else:
        print("No rules enabled.")
        return

    path_list = glob.glob(args.glob, recursive=True)
    total = len(path_list)
    for i, path in enumerate(path_list, 1):
        print(f"Processing {i}/{total}\t{path}  ", end="\r")

        file = File(path)
        file.apply_rules(rules)

        if args.fix:
            file.write_back()

    print()

    # Show the statistics.
    print(f"Total checked files: {total}")
    for rule in rules:
        print(f"    {rule.colored_rule_name}:\t{rule.count}")


if __name__ == "__main__":
    main()
