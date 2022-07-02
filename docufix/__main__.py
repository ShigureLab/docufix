import argparse
import glob

from .rules import InsertWhitespaceBetweenCnAndEnCharRule, TrimTrailingWhitespace


def main() -> None:
    rule_clss = [
        InsertWhitespaceBetweenCnAndEnCharRule,
        TrimTrailingWhitespace,
    ]

    parser = argparse.ArgumentParser()
    parser.add_argument("glob", help="Path glob to check")
    parser.add_argument("--fix", help="Auto fix the wrongs", action="store_true")
    for rule_cls in rule_clss:
        rule_cls.extend_cli(parser)
    args = parser.parse_args()

    rules = [rule_cls(args) for rule_cls in rule_clss]
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

    line_rules = [rule for rule in rules if "line" in rule.rule_type]
    file_rules = [rule for rule in rules if "file" in rule.rule_type]

    path_list = glob.glob(args.glob, recursive=True)
    total = len(path_list)
    for i, path in enumerate(path_list, 1):
        print(f"Processing {i}/{total}", end="\r")

        formatted_text = ""

        with open(path, "r", encoding="utf-8", newline="\n") as f:
            # Line rules.
            for lineno, line in enumerate(f, 1):
                for rule in line_rules:
                    if (lint_result := rule.lint_line(line)) is not None:
                        highlight_string, colno = lint_result
                        print(f"{rule.colored_rule_name}\t{path}:{lineno}:{colno}\t\t{highlight_string}")
                    line = rule.format_line(line)
                formatted_text += line

        # File rules.
        for rule in file_rules:
            if rule.lint_file(formatted_text):
                print(f"{rule.colored_rule_name}\t{path}")
            formatted_text = rule.format_file(formatted_text)

        if args.fix:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(formatted_text)

    print()

    print(f"Total checked files: {total}")
    for rule in rules:
        print(f"    {rule.colored_rule_name}:\t{rule.count}")


if __name__ == "__main__":
    main()
