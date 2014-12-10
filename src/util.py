def isBlackKey(pitch):

    remainder = pitch % 12
    return (
        remainder == 1 or
        remainder == 3 or
        remainder == 6 or
        remainder == 8 or
        remainder == 10)

