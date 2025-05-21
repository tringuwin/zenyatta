import pytest
from exceptions import CommandError
from helpers import can_be_int, convert_to_int, verify_params_in_string, is_valid_hex_code

def test_can_be_int():

    assert can_be_int('123') is True
    assert can_be_int('not_int') is False
    assert can_be_int('123.45') is False
    assert can_be_int('') is False
    assert can_be_int(' ') is False
    assert can_be_int(None) is False

def test_is_valid_hex_code():

    assert is_valid_hex_code('#abc') is True
    assert is_valid_hex_code('abc') is True
    assert is_valid_hex_code('#abcdef') is True
    assert is_valid_hex_code('abcdef') is True
    assert is_valid_hex_code('#123456') is True
    assert is_valid_hex_code('123456') is True
    assert is_valid_hex_code('#xyz') is False
    assert is_valid_hex_code('xyz') is False
    assert is_valid_hex_code('#12345g') is False
    assert is_valid_hex_code('12345g') is False
    assert is_valid_hex_code('#1234') is False


def test_verify_params_in_string():

    assert verify_params_in_string('param1 param2 param3', 3) == ['param1', 'param2', 'param3']

    with pytest.raises(CommandError, match='Invalid number of parameters. Expected 3, got 2.'):
        verify_params_in_string('param1 param2', 3)


def test_convert_to_int():

    assert convert_to_int('123') == 123

    with pytest.raises(CommandError, match='Invalid value: not_int is not an integer.'):
        convert_to_int('not_int')
