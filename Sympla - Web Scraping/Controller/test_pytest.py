import pytest

from controllerTest import conTest


def test_answer_convertMes_01():
    con = conTest()
    assert con.convertMes('janeiro') == 'janeiro'


def test_answer_convertMes_02():
    con = conTest()
    assert con.convertMes('janeiro') == '01'


def test_answer_convertMes_03():
    con = conTest()
    assert con.convertMes('janeiro') == 1