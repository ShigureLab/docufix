import argparse
import glob

from .core import File, Rule
from .rules import (
    EnsureFinalNewlineRule,
    InsertWhitespaceBetweenCnAndEnCharRule,
    ReplaceTabWithSpaceRule,
    TrimTrailingBlankLinesRule,
    TrimTrailingWhitespace,
    UnifyNewlineRule,
)


def resolve_globs(globs: list[str], ignore_globs: list[str]) -> list[str]:
    ignore_paths_list = [glob.glob(ignore_glob, recursive=True) for ignore_glob in ignore_globs]
    ignore_paths = [path for ignore_paths in ignore_paths_list for path in ignore_paths]

    paths_list = [glob.glob(glob_, recursive=True) for glob_ in globs]
    paths = [path for paths in paths_list for path in paths if path not in ignore_paths]
    return paths


def main() -> None:
    rule_clss = [
        InsertWhitespaceBetweenCnAndEnCharRule,
        TrimTrailingWhitespace,
        UnifyNewlineRule,
        EnsureFinalNewlineRule,
        TrimTrailingBlankLinesRule,
        ReplaceTabWithSpaceRule,
    ]

    parser = argparse.ArgumentParser()
    parser.add_argument("globs", help="Path glob to check", nargs="+")
    parser.add_argument("--fix", help="Auto fix the wrongs", action="store_true")
    parser.add_argument("--ignore-globs", help="Path glob to ignore, comma separated", type=str, default="")
    parser.add_argument("--all-rules", action="store_true", help="Apply all existing rules")
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

    path_list = resolve_globs(args.globs, args.ignore_globs.split(","))
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
