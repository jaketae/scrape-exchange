import pytest


def test_parse():
    import random
    import string
    from app.utils import parse

    assert parse("") == ""
    assert parse("Ipad pro") == "Ipad+pro"
    assert parse("Macbook pro 13 inch 512 gb") == "Macbook+pro+13+inch+512+gb"


def test_floatify():
    from app.utils import floatify

    assert floatify("$1,234") == 1234
    assert floatify("$123.00-$456.00") == 456
    assert floatify("$1000") == 1000
    assert floatify("None") == 0


def test_stringify():
    from app.utils import stringify

    assert (
        stringify(["ipad", "airpods"], ["some text", "some text"])
        == "ipad: Price not available\n\nairpods: Price not available\n"
    )
    assert stringify([], []) == "There are no results to show."
    assert (
        stringify(["ipad", "airpods"], ["$10", "$10"])
        == "ipad: $10\n\nairpods: $10\n"
    )


def test_redirect():
    from app.utils import redirect

    assert redirect("https://www.google.com") == "https://www.google.com"
    assert (
        redirect(
            (
                "https://l.messenger.com/l.php?u=https%3A%2F%2Fwww.shopmyexchange.com%2F"
                "apple-ipad-pro-11-in-512gb-with-wifi%2F1726804&h=AT3GRFe-SvZbNUTx-"
                "XLVVEWhEy8eBs_QOtd13einBQXNWit63zN5UrP8H1GsR8Y8gdUr6MnH6ry7gvfSD5gH"
                "YeGlQZQkp7mJiLhQlJysrEmwA7jcfgJTDVYYJK8smh-ICJx1BcdvHQ"
            )
        )
        == "https://www.shopmyexchange.com/apple-ipad-pro-11-in-512gb-with-wifi/1726804"
    )
