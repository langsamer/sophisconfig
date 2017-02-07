'''
Created on Feb 7, 2017

@author: malte
'''
# import pytest

from sophconf.configoptions import Option


def test_option_instantiate1():
    o = Option(name='weight', value=32.1, typ=int)
    assert o() == 32
    assert o.name == 'weight'
    assert o.typ == int


def test_option_instantiate2():
    o = Option(name='weight', value=0.9, typ=float)
    assert o() == 0.9


def test_option_instantiate3():
    o = Option(name='weight', value=7, typ=float)
    assert o() == 7.0
    assert type(o()) == float


def test_option_set1():
    o = Option(name='weight', value=32.1, typ=int)
    o.value = 43.5
    assert o() == 43
