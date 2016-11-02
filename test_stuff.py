from app import *


def do_thing(thing):
    return thing

def test_useless():
    assert do_thing("cake") == "cake"
    assert do_thing("not_cake") != "cake"

def test_useless2():
    assert 1 == 1
