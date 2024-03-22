import utils.parse as parse

def test_1():
    assert parse.tokenize_line("hello world") == [ "hello", "world" ]
    assert parse.tokenize_line("hello  world ") == [ "hello", "world" ]
    assert parse.tokenize_line(" hello  world ") == [ "hello", "world" ]
    assert parse.tokenize_line("\"hello\" world ") == [ "\"hello\"", "world" ]
    assert parse.tokenize_line("this \"is a \" test") == [ "this", "\"is a \"", "test" ]
    assert parse.tokenize_line("this \"is a\" test ; Comment stuff here") == [ "this", "\"is a\"", "test" ]
    assert parse.tokenize_line("  ; Comment stuff here") == [ ]
    assert parse.tokenize_line("this \"is a;\" test ; Comment stuff here") == [ "this", "\"is a;\"", "test" ]
    assert parse.tokenize_line("") == [ ]
    assert parse.tokenize_line("M001=00") == [ "M001", "=", "00" ]
    assert parse.tokenize_line("M001  =00") == [ "M001", "=", "00" ]
    assert parse.tokenize_line("M001=  00") == [ "M001", "=", "00" ]

def test_2():

    named_c = dict()
    named_c["a"] = [ "MPW", "15", "*" ]
    assert parse.expand_tokens(named_c, ["a", "00"]) == ["MPW", "15", "*", "00" ]

    # Show the double-expansion
    named_c["MPW"] = [ "99" ]
    assert parse.expand_tokens(named_c, ["a", "00"]) == ["99", "15", "*", "00" ]

def test_3():
    assert not parse.is_valid_dtmf_symbol("E")

