from itertools import combinations

from src.model import *
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

                # Currently, we don't support the case of crossed fingers in an assignment for a
                # single score state, and thus all candidate assignments generated are in finger
                # order. (We of course support the case of crossed fingers from one score state
                # to the next.
                assignments = list(combinations([1, 2, 3, 4, 5], len(pitches)))

                toRemove = []
                for p in heldPitches:
                    for a in assignments:
                        fingerAssignedToHeldPitch = a[pitches.index(p)]
                        fingerThatPressedHeldPitch = prevFS.getFingerByPitch(p)
                        if (fingerAssignedToHeldPitch != fingerThatPressedHeldPitch):
                            toRemove.append(a)
                for a in toRemove:
                    assignments.remove(a)

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

    def getVertCost(self, pitches, assignment):

        assert len(pitches) == len(assignment)

        if len(pitches) == 1:
            return 0

        # Totals up the costs for adjacent pairs in the assignment
        totalCost = 0.0
        for i in range(0, len(pitches) - 1):
            span = pitches[i + 1] - pitches[i]
            if span not in pairSpanCost[(assignment[i], assignment[i + 1])]:
                pairCost = float('inf')
            else:
                pairCost = pairSpanCost[(assignment[i], assignment[i + 1])][span]
            totalCost += pairCost

        return totalCost