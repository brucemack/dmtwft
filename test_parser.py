import utils.parse as parse
from utils.Token import Token

def test_1():

    assert parse.tokenize_line("hello world") == [ Token("hello"), Token("world") ]
    assert parse.tokenize_line("hello  world ") == [ Token("hello"), Token("world") ]
    assert parse.tokenize_line(" hello  world ") == [ Token("hello"), Token("world") ]
    assert parse.tokenize_line("\"hello\" world ") == [ Token("hello", is_quoted=True), Token("world") ]
    assert parse.tokenize_line("this \"is a \" test") == [ Token("this"), Token("is a ", is_quoted=True), Token("test") ]
    assert parse.tokenize_line("this \"is a \" test ; Comment stuff here") == \
        [ Token("this"), Token("is a ", is_quoted=True), Token("test") ]
    assert parse.tokenize_line("  ; Comment stuff here") == [ ]
    assert parse.tokenize_line("") == [ ]
    assert parse.tokenize_line("this \"is a;\" test ; Comment stuff here") == \
        [ Token("this"), Token("is a;", is_quoted=True), Token("test") ]
    assert parse.tokenize_line("M001=00") == [ Token("M001"), Token("="), Token("00") ]
    assert parse.tokenize_line("M001  =00") == [ Token("M001"), Token("="), Token("00") ]
    assert parse.tokenize_line("M001=  00") == [ Token("M001"), Token("="), Token("00") ]
    assert parse.tokenize_line("hello world*") == [ Token("hello"), Token("world"), Token("*") ]

def test_2():

    named_c = dict()

    named_c["a"] = [ Token("MPW"), Token("15"), Token("*") ]
    assert parse.expand_tokens(named_c, [ Token("a"), Token("00") ]) == \
        [ Token("MPW"), Token("15"), Token("*"), Token("00") ]

    # Show the double-expansion
    named_c["MPW"] = [ Token("99") ]
    assert parse.expand_tokens(named_c, [ Token("a"), Token("00") ]) == \
        [ Token("99"), Token("15"), Token("*"), Token("00") ]

def test_3():
    assert not parse.is_valid_dtmf_symbol("E")

