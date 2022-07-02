import argparse
import glob
import re
from typing import Optional

CSI = "\x1b["
RED = f"{CSI}31m"
CYAN = f"{CSI}36m"
BLUE = f"{CSI}34m"
CLR = f"{CSI}0m"

REGEX_CN_CHAR_STR = r"[\u4e00-\u9fa5]"
REGEX_EN_CHAR_STR = r"[a-zA-Z0-9]"

REGEX_CN_WITH_EN = re.compile(f"(?P<cn>{REGEX_CN_CHAR_STR})(?P<en>{REGEX_EN_CHAR_STR})")
REGEX_EN_WITH_CN = re.compile(f"(?P<en>{REGEX_EN_CHAR_STR})(?P<cn>{REGEX_CN_CHAR_STR})")


def check_string(string: str) -> Optional[tuple[str, int]]:
    min_start = 999999
    max_end = -1
    found = False
    for mth in REGEX_CN_WITH_EN.finditer(string):
        found = True
        start, end = mth.span()
        min_start = min(min_start, start)
        max_end = max(max_end, end)
    for mth in REGEX_EN_WITH_CN.finditer(string):
        found = True
        start, end = mth.span()
        min_start = min(min_start, start)
        max_end = max(max_end, end)

    if not found:
        return None

    start = max(0, min_start - 10)
    end = min(len(string), max_end + 10, start + 40)

    string = string.rstrip("\n")
    string = string[start:end]
    string = REGEX_EN_WITH_CN.sub(rf"{BLUE}\g<en>\g<cn>{CLR}", string)
    string = REGEX_CN_WITH_EN.sub(rf"{RED}\g<cn>\g<en>{CLR}", string)
    return string, min_start


def format_string(string: str) -> str:
    string = REGEX_CN_WITH_EN.sub(r"\g<cn> \g<en>", string)
    string = REGEX_EN_WITH_CN.sub(r"\g<en> \g<cn>", string)
    return string


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("glob", help="Path glob to check")
    parser.add_argument("--fix", help="Auto fix the wrongs", action="store_true")
    args = parser.parse_args()
    path_list = glob.glob(args.glob, recursive=True)
    total = len(path_list)

    for i, path in enumerate(path_list, 1):
        print(f"Processing {i}/{total}", end="\r")

        formatted_text = ""
        with open(path, "r", encoding="utf-8", newline="\n") as f:
            for lineno, line in enumerate(f, 1):
                if (check_result := check_string(line)) is not None:
                    highlight_string, colno = check_result
                    print(f"{path}:{lineno}:{colno}\t\t\t{highlight_string}")
                formatted_text += format_string(line)

        if args.fix:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(formatted_text)


def test_cases():
    assert re.search(REGEX_CN_CHAR_STR, "纯中文") is not None
    assert re.search(REGEX_EN_CHAR_STR, "纯中文") is None
    assert re.search(REGEX_CN_CHAR_STR, "，") is None
    assert REGEX_CN_WITH_EN.search("纯中文") is None
    assert REGEX_EN_WITH_CN.search("纯中文") is None

    assert re.search(REGEX_EN_CHAR_STR, "Pure English") is not None
    assert re.search(REGEX_CN_CHAR_STR, "Pure English") is None
    assert REGEX_CN_WITH_EN.search("Pure English") is None
    assert REGEX_EN_WITH_CN.search("Pure English") is None

    assert REGEX_CN_WITH_EN.search("中文后面带English") is not None
    assert REGEX_CN_WITH_EN.sub(r"\g<cn> \g<en>", "中文后面带English") == "中文后面带 English"
    assert REGEX_CN_WITH_EN.sub(r"\g<cn> \g<en>", "中文后面带English啦") == "中文后面带 English啦"

    assert REGEX_EN_WITH_CN.search("English with中文字符") is not None
    assert REGEX_EN_WITH_CN.sub(r"\g<en> \g<cn>", "English with中文字符") == "English with 中文字符"
    assert REGEX_EN_WITH_CN.sub(r"\g<en> \g<cn>", "呀English with 中文字符") == "呀English with 中文字符"

    assert REGEX_CN_WITH_EN.sub(r"\g<cn> \g<en>", "带上标点符号试试，en。") == "带上标点符号试试，en。"
    assert REGEX_EN_WITH_CN.sub(r"\g<en> \g<cn>", "带上标点符号试试，en。") == "带上标点符号试试，en。"

    long_text_unformatted = """
    这是一段长文本，会混杂一些英文
    啦啦啦，char喵喵喵en啊啦啦啦。xxxx
    en，char。
    """
    long_text_formatted = """
    这是一段长文本，会混杂一些英文
    啦啦啦，char 喵喵喵 en 啊啦啦啦。xxxx
    en，char。
    """
    assert format_string(long_text_unformatted) == long_text_formatted


if __name__ == "__main__":
    # test_cases()
    main()
