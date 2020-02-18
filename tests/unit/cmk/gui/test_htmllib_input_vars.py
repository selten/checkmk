#!/usr/bin/env python
# encoding: utf-8

import pytest  # type: ignore
import six

from cmk.gui.exceptions import MKUserError
from cmk.gui.globals import html


@pytest.fixture()
def set_vars(register_builtin_html):
    html.request.set_var("xyz", "x")
    html.request.set_var("abc", "äbc")


@pytest.fixture()
def set_int_vars(register_builtin_html):
    html.request.set_var("number", "2")
    html.request.set_var("float", "2.2")
    html.request.set_var("not_a_number", "a")


@pytest.mark.usefixtures("set_vars")
def test_get_str_input_type():
    assert html.get_str_input("xyz") == "x"
    assert isinstance(html.get_str_input("xyz"), str)


@pytest.mark.usefixtures("set_vars")
def test_get_str_input_non_ascii():
    assert html.get_str_input("abc") == b"äbc"


@pytest.mark.usefixtures("set_vars")
def test_get_str_input_default():
    assert html.get_str_input("get_default", "xyz") == "xyz"
    assert html.get_str_input("zzz") is None


@pytest.mark.usefixtures("set_vars")
def test_get_str_input_mandatory_input_type():
    assert html.get_str_input_mandatory("xyz") == "x"
    assert isinstance(html.get_str_input_mandatory("xyz"), str)


@pytest.mark.usefixtures("set_vars")
def test_get_str_input_mandatory_non_ascii():
    assert html.get_str_input_mandatory("abc") == b"äbc"


@pytest.mark.usefixtures("set_vars")
def test_get_str_input_mandatory_default():
    assert html.get_str_input_mandatory("get_default", "xyz") == "xyz"

    with pytest.raises(MKUserError, match="is missing"):
        html.get_str_input_mandatory("zzz")


@pytest.mark.usefixtures("set_vars")
def test_get_ascii_input_input_type():
    assert html.get_ascii_input("xyz") == "x"
    assert isinstance(html.get_ascii_input("xyz"), str)


@pytest.mark.usefixtures("set_vars")
def test_get_ascii_input_non_ascii():
    with pytest.raises(MKUserError) as e:
        html.get_ascii_input("abc")
    assert "must only contain ASCII" in "%s" % e


@pytest.mark.usefixtures("set_vars")
def test_get_ascii_input_default():
    assert html.get_ascii_input("get_default", "xyz") == "xyz"
    assert html.get_ascii_input("zzz") is None


@pytest.mark.usefixtures("set_vars")
def test_get_ascii_input_mandatory_input_type():
    assert html.get_ascii_input_mandatory("xyz") == "x"
    assert isinstance(html.get_ascii_input_mandatory("xyz"), str)


@pytest.mark.usefixtures("set_vars")
def test_get_ascii_input_mandatory_non_ascii():
    with pytest.raises(MKUserError) as e:
        html.get_ascii_input_mandatory("abc")
    assert "must only contain ASCII" in "%s" % e


@pytest.mark.usefixtures("set_vars")
def test_get_ascii_input_mandatory_default():
    assert html.get_ascii_input_mandatory("get_default", "xyz") == "xyz"

    with pytest.raises(MKUserError, match="is missing"):
        html.get_ascii_input_mandatory("zzz")


@pytest.mark.usefixtures("set_vars")
def test_get_unicode_input_type():
    assert html.get_unicode_input("xyz") == "x"
    assert isinstance(html.get_unicode_input("xyz"), six.text_type)


@pytest.mark.usefixtures("set_vars")
def test_get_unicode_input_non_ascii():
    assert html.get_unicode_input("abc") == u"äbc"


@pytest.mark.usefixtures("set_vars")
def test_get_unicode_input_default():
    assert html.get_unicode_input("get_default", u"xyz") == u"xyz"
    assert html.get_unicode_input("zzz") is None


@pytest.mark.usefixtures("set_vars")
def test_get_unicode_input_mandatory_input_type():
    assert html.get_unicode_input_mandatory("xyz") == u"x"
    assert isinstance(html.get_unicode_input_mandatory("xyz"), six.text_type)


@pytest.mark.usefixtures("set_vars")
def test_get_unicode_input_mandatory_non_ascii():
    assert html.get_unicode_input_mandatory("abc") == u"äbc"


@pytest.mark.usefixtures("set_vars")
def test_get_unicode_input_mandatory_default():
    assert html.get_unicode_input_mandatory("get_default", u"xyz") == u"xyz"

    with pytest.raises(MKUserError, match="is missing"):
        html.get_unicode_input_mandatory("zzz")


@pytest.mark.usefixtures("set_int_vars")
def test_get_integer_input_default():
    assert html.get_integer_input("not_existing") is None
    assert html.get_integer_input("get_default", 1) == 1
    assert html.get_integer_input("bla") is None


@pytest.mark.usefixtures("set_int_vars")
def test_get_integer_input_regular():
    assert html.get_integer_input("number") == 2


@pytest.mark.usefixtures("set_int_vars")
def test_get_integer_input_float():
    with pytest.raises(MKUserError) as e:
        html.get_integer_input("float")
    assert "is not an integer" in "%s" % e


@pytest.mark.usefixtures("set_int_vars")
def test_get_integer_input_not_a_number():
    with pytest.raises(MKUserError) as e:
        html.get_integer_input("not_a_number")
    assert "is not an integer" in "%s" % e


@pytest.mark.usefixtures("set_int_vars")
def test_get_integer_input_mandatory_default():
    with pytest.raises(MKUserError) as e:
        html.get_integer_input_mandatory("not_existing")
    assert "is missing" in "%s" % e

    assert html.get_integer_input_mandatory("get_default", 1) == 1

    with pytest.raises(MKUserError) as e:
        html.get_integer_input_mandatory("bla")
    assert "is missing" in "%s" % e


@pytest.mark.usefixtures("set_int_vars")
def test_get_integer_input_mandatory_regular():
    assert html.get_integer_input_mandatory("number") == 2


@pytest.mark.usefixtures("set_int_vars")
def test_get_integer_input_mandatory_float():
    with pytest.raises(MKUserError) as e:
        html.get_integer_input_mandatory("float")
    assert "is not an integer" in "%s" % e


@pytest.mark.usefixtures("set_int_vars")
def test_get_integer_input_mandatory_not_a_number():
    with pytest.raises(MKUserError) as e:
        html.get_integer_input_mandatory("not_a_number")
    assert "is not an integer" in "%s" % e


@pytest.mark.parametrize("invalid_url", [
    "http://localhost/",
    "://localhost",
    "localhost:80/bla",
])
def test_get_url_input_invalid_urls(register_builtin_html, invalid_url):
    html.request.set_var("varname", invalid_url)

    with pytest.raises(MKUserError) as e:
        html.get_url_input("varname")
    assert "not a valid URL" in "%s" % e


def test_get_url_input(register_builtin_html):
    html.request.set_var("url", "view.py?bla=blub")
    html.request.set_var("no_url", "2")
    html.request.set_var("invalid_url", "http://bla/")
    html.request.set_var("invalid_char", "viäw.py")
    html.request.set_var("invalid_char2", "vi+w.py")

    with pytest.raises(MKUserError) as e:
        html.get_url_input("not_existing")
    assert "is missing" in "%s" % e

    assert html.get_url_input("get_default", "my_url.py") == "my_url.py"
    assert html.get_url_input("get_default", "http://bla/") == "http://bla/"
    assert html.get_url_input("url") == "view.py?bla=blub"
    assert html.get_url_input("no_url") == "2"

    with pytest.raises(MKUserError) as e:
        html.get_url_input("invalid_url")
    assert "not a valid" in "%s" % e

    with pytest.raises(MKUserError) as e:
        html.get_url_input("invalid_char")
    assert "not a valid" in "%s" % e

    with pytest.raises(MKUserError) as e:
        html.get_url_input("invalid_char2")
    assert "not a valid" in "%s" % e

    assert html.get_url_input("no_url") == "2"
