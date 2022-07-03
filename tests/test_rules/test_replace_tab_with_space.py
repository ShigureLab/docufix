from docufix.rules.replace_tab_with_space import format


def test_format():
    assert format("\t111", 4) == "    111"
    assert format("1\t111", 2) == "1 111"
    assert format("12\t111", 4) == "12  111"
    assert format("12\t\t111", 4) == "12      111"
    assert format("12\t\t11\t1", 4) == "12      11  1"
    assert format("", 4) == ""
    assert format(" ", 4) == " "
    assert format("\t", 4) == "    "
    assert format("\t\t", 4) == "        "
