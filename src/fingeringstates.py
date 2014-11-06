from itertools import combinations
from collections import defaultdict
from model import *
from parameters import *

class FingeringStateGenerator(object):

    def __init__(self, startSS):

        self.currentSS = startSS
        self.prevSS = None

        self.startFS = FingeringState(None, (), 0)
        self.prevFSs = [self.startFS]

        self.allFSs = [self.startFS]

    def generateFingeringStates(self):

        while self.currentSS is not None:

            pitches = self.currentSS.getPitches()
            heldPitches = self.currentSS.getHeldPitches()

            usedAssignmentsMapToFS = dict()
            fingeringStatesForCurrentSS = []

            for prevFS in self.prevFSs:

                availableFingers = [1, 2, 3, 4, 5]
                for f in prevFS.fingers:
                    availableFingers.remove(f)
                if self.prevSS is None:
                    prevPitches = []
                else:
                    prevPitches = self.prevSS.getPitches()
                for prevP in prevPitches:
                    if prevP in pitches:
                        assert prevFS.getFingerByPitch(prevP) not in availableFingers
                        availableFingers.append(prevFS.getFingerByPitch(prevP))
                availableFingers.sort()

                # Currently, we don't support the case of crossed fingers in an assignment for a
                # single score state, and thus all candidate assignments generated are in finger
                # order. (We of course support the case of crossed fingers from one score state
                # to the next.
                assignments = list(combinations(availableFingers, len(pitches)))

                self.removeInvalidAssignmentsToHeldPitches(assignments, pitches, heldPitches, prevFS)

                for a in assignments:

                    if a in usedAssignmentsMapToFS:
                        fs = usedAssignmentsMapToFS[a]
                    else:
                        vertCost = self.getVertCost(pitches, a)

                        if vertCost == float('inf'):
                            continue

                        fs = FingeringState(self.currentSS, a, vertCost)
                        usedAssignmentsMapToFS[a] = fs
                        fingeringStatesForCurrentSS.append(fs)
                        self.allFSs.append(fs)

                    prevFS.children.append(fs)

            self.prevFSs = fingeringStatesForCurrentSS

            self.prevSS = self.currentSS
            self.currentSS = self.currentSS.next

        return self.allFSs

    def removeInvalidAssignmentsToHeldPitches(self, assignments, pitches, heldPitches, prevFS):
        toRemove = []
        for p in heldPitches:
            for a in assignments:
                fingerAssignedToHeldPitch = a[pitches.index(p)]
                fingerThatPressedHeldPitch = prevFS.getFingerByPitch(p)
                if (fingerAssignedToHeldPitch != fingerThatPressedHeldPitch):
                    toRemove.append(a)
        for a in toRemove:
            assignments.remove(a)

    def getVertCost(self, pitches, assignment):

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

    def getHorizCost(self, prevPitches, prevAssignment, currPitches, currAssignment):

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

        print horizPitchPairs

        membersOfHorizPitchPairs = []
        for pair in horizPitchPairs:
            for m in pair:
                membersOfHorizPitchPairs.append(m)
        membersOfHorizPitchPairs = sorted(list(set(membersOfHorizPitchPairs)))

        print membersOfHorizPitchPairs

        totalCost = 0.0
        for i in range(0, len(membersOfHorizPitchPairs) - 1):

            print (membersOfHorizPitchPairs[i], membersOfHorizPitchPairs[i + 1])

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
            else:
                pairCost = pairSpanCost[assignment][span]

            totalCost += pairCost

        return totalCost