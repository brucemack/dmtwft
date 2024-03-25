import uuid
import utils.parse as parse
import utils.DTMF as DTMF
from utils.Token import Token
import utils.convert as convert 
import utils.sessions as sessions

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

def test_sessions():

    def get_default_session():
        s = dict()
        s["url_file"] = ""
        s["contents"] = None
        s["mpw"] = "99"
        s["cpw"] = "99"
        s["apw"] = "99"
        s["rbpw"] = "99"
        s["warminit"] = "on"
        s["tone_dur"] = "75"
        s["gap_dur"] = "75"
        s["sound"] = None
        s["message"] = None
        return s

    sessions.set_max_sessions(2)
    assert sessions.get_session_count() == 0
    sessions.get_session("A", get_default_session)
    assert sessions.get_session_count() == 1
    sessions.get_session("B", get_default_session)
    assert sessions.get_session_count() == 2
    sessions.get_session("C", get_default_session)
    assert sessions.get_session_count() == 2
