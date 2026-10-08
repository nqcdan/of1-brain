from hello import hello


def test_default_greeting():
    assert hello() == "Hello, World!"


def test_named_greeting():
    assert hello("Dan") == "Hello, Dan!"


def test_blank_name_falls_back():
    assert hello("") == "Hello, World!"
    assert hello("   ") == "Hello, World!"
