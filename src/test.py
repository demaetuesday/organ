from util import *

def isBlackKeyTest():

    assert isBlackKey(22)
    assert isBlackKey(25)
    assert isBlackKey(27)
    assert isBlackKey(30)
    assert isBlackKey(32)
    assert isBlackKey(34)
    assert isBlackKey(37)

    assert isBlackKey(58)
    assert isBlackKey(61)
    assert isBlackKey(63)
    assert isBlackKey(66)
    assert isBlackKey(68)
    assert isBlackKey(70)
    assert isBlackKey(73)

    assert not isBlackKey(23)
    assert not isBlackKey(24)
    assert not isBlackKey(26)
    assert not isBlackKey(28)
    assert not isBlackKey(29)
    assert not isBlackKey(31)
    assert not isBlackKey(33)
    assert not isBlackKey(35)
    assert not isBlackKey(36)

    assert not isBlackKey(59)
    assert not isBlackKey(60)
    assert not isBlackKey(62)
    assert not isBlackKey(64)
    assert not isBlackKey(65)
    assert not isBlackKey(67)
    assert not isBlackKey(69)
    assert not isBlackKey(71)
    assert not isBlackKey(72)

isBlackKeyTest()
