from itertools import combinations
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

            currPitches = self.currentSS.getPitches()

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
                    if prevP in currPitches:
                        assert prevFS.getFingerByPitch(prevP) not in availableFingers
                        availableFingers.append(prevFS.getFingerByPitch(prevP))
                availableFingers.sort()

                # Currently, we don't support the case of crossed fingers in an assignment for a
                # single score state, and thus all candidate assignments generated are in finger
                # order. (We of course support the case of crossed fingers from one score state
                # to the next.
                assignments = list(combinations(availableFingers, len(currPitches)))

                heldPitches = self.currentSS.getHeldPitches()
                for p in currPitches:
                    if self.isSopranoToAltoExchange(p, currPitches, prevPitches):
                        if p not in heldPitches:
                            heldPitches.append(p)
                            heldPitches.sort()
                    if self.isAltoToSopranoExchange(p, currPitches, prevPitches):
                        if p in heldPitches:
                            heldPitches.remove(p)

                toRemove = []
                for a in assignments:
                    if self.isInvalidAssignmentForHeldPitch(currPitches, heldPitches, a, prevFS):
                        toRemove.append(a)
                for a in toRemove:
                    assignments.remove(a)

                for a in assignments:

                    if prevFS.scoreState is None:
                        horizCost = 0.0
                    else:
                        horizCost = self.getHorizCost(prevFS.scoreState.getPitches(), prevFS.fingers,
                                                      currPitches, a)
                    if horizCost ==  float('inf'):
                        continue

                    if a in usedAssignmentsMapToFS:
                        fs = usedAssignmentsMapToFS[a]
                        child = (fs, horizCost)
                    else:
                        vertCost = self.getVertCost(currPitches, a)

                        if vertCost == float('inf'):
                            continue

                        fs = FingeringState(self.currentSS, a, vertCost)
                        child = (fs, horizCost)

                        usedAssignmentsMapToFS[a] = fs
                        fingeringStatesForCurrentSS.append(fs)
                        self.allFSs.append(fs)

                    prevFS.children.append(child)

            self.prevFSs = fingeringStatesForCurrentSS

            self.prevSS = self.currentSS
            self.currentSS = self.currentSS.next

        goalFS = FingeringState(None, (), 0)
        for prevFS in self.prevFSs:
            prevFS.children.append((goalFS, 0))
        self.allFSs.append(goalFS)

        return self.allFSs

    def isInvalidAssignmentForHeldPitch(self, pitches, heldPitches, assignment, prevFS):

        for p in heldPitches:
            fingerAssignedToHeldPitch = assignment[pitches.index(p)]
            fingerThatPressedHeldPitch = prevFS.getFingerByPitch(p)
            if (fingerAssignedToHeldPitch != fingerThatPressedHeldPitch):
                return True
        return False

    def isSopranoToAltoExchange(self, pitch, currPitches, prevPitches):

        if len(prevPitches) == 0:
            return False
        # if this pitch == the soprano pitch in the previous SS, and
        # this pitch != the soprano pitch in the current SS
        return pitch == prevPitches[-1] and pitch != currPitches[-1]

    def isAltoToSopranoExchange(self, pitch, currPitches, prevPitches):

        if len(prevPitches) == 0:
            return False
        # if this pitch != the soprano pitch in the previous SS, and
        # this pitch == the soprano pitch in the current SS
        return pitch != prevPitches[-1] and pitch == currPitches[-1]

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
            else:
                pairCost = pairSpanCost[assignment][span]

            totalCost += pairCost

        return totalCost / (len(membersOfHorizPitchPairs) - 1)