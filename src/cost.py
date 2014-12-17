from itertools import combinations
from parameters import *
from util import *

def getVertCost(pitches, assignment):

    assert len(pitches) == len(assignment)

    if len(pitches) == 1:
        return 0

    # Totals up the costs of pairs consisting of neighboring elements in the set of pitches.
    totalCost = 0.0
    for i in range(0, len(pitches) - 1):
        span = pitches[i + 1] - pitches[i]
        if span not in pairSpanCost[(assignment[i], assignment[i + 1])]:
            pairCost = float('inf')
        else:
            pairCost = pairSpanCost[(assignment[i], assignment[i + 1])][span]
        totalCost += pairCost

    return totalCost

def getHorizCost(prevPitches, prevAssignment, currPitches, currAssignment):

    assert len(prevPitches) == len(prevAssignment)
    assert len(currPitches) == len(currAssignment)

    prevPitchPairs = list(combinations(prevPitches, 2))
    currPitchPairs = list(combinations(currPitches, 2))

    # Finds the set of horizontal pitch pairs, which is the set of pitch pairs that have one
    # pitch from the previous SS and one pitch from the current SS, and that are not already
    # present as a pair in the pitches from the previous SS alone or in the pitches from the
    # current score state alone.
    allPitches = sorted(list(set(prevPitches + currPitches)))
    horizPitchPairs = list(combinations(allPitches, 2))
    toRemove = []
    for pair in horizPitchPairs:
        if pair in prevPitchPairs or pair in currPitchPairs:
            toRemove.append(pair)
    for pair in toRemove:
        horizPitchPairs.remove(pair)
    #print horizPitchPairs

    membersOfHorizPitchPairs = []
    for pair in horizPitchPairs:
        for m in pair:
            membersOfHorizPitchPairs.append(m)
    membersOfHorizPitchPairs = sorted(list(set(membersOfHorizPitchPairs)))
    #print membersOfHorizPitchPairs

    totalCost = 0.0
    for i in range(0, len(membersOfHorizPitchPairs) - 1):

        #print (membersOfHorizPitchPairs[i], membersOfHorizPitchPairs[i + 1])
        span = membersOfHorizPitchPairs[i + 1] - membersOfHorizPitchPairs[i]
        assert span > 0

        mI = membersOfHorizPitchPairs[i]
        if mI in prevPitches:
            assert mI not in currPitches
            fingerA = prevAssignment[prevPitches.index(mI)]
        elif mI in currPitches:
            assert mI not in prevPitches
            fingerA = currAssignment[currPitches.index(mI)]

        mIPlus1 = membersOfHorizPitchPairs[i + 1]
        if mIPlus1 in prevPitches:
            assert mIPlus1 not in currPitches
            fingerB = prevAssignment[prevPitches.index(mIPlus1)]
        elif mIPlus1 in currPitches:
            assert mIPlus1 not in prevPitches
            fingerB = currAssignment[currPitches.index(mIPlus1)]

        if fingerA > fingerB:
            assignment = (fingerB, fingerA)
            span *= -1
        else:
            assignment = (fingerA, fingerB)

        if span not in pairSpanCost[assignment]:
            pairCost = float('inf')
        # elif isInvalidAssignmentWithBlackKey([mI, mIPlus1], assignment, span):
        #     pairCost = float('inf')
        else:
            pairCost = pairSpanCost[assignment][span]

        totalCost += pairCost

        if isFingerChangeOnSameNote(prevPitches, prevAssignment, currPitches, currAssignment):
            totalCost += fingerChangeCost

    return totalCost / (len(membersOfHorizPitchPairs) - 1)

def isInvalidAssignmentWithBlackKey(pitches, assignment, span):

    if span > 0 or 1 in assignment:
        return False
    return isBlackKey(pitches[0])

def isFingerChangeOnSameNote(prevPitches, prevAssignment, currPitches, currAssignment):

    for prevPitch in prevPitches:
        for currPitch in currPitches:
            if prevPitch == currPitch:
                if (prevAssignment[prevPitches.index(prevPitch)] !=
                        currAssignment[currPitches.index(currPitch)]):
                    return True
    return False