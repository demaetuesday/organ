from model import *
from cost import *

class FingeringStateGenerator(object):

    def __init__(self, startSS):

        self.currentSS = startSS
        self.prevSS = None

        self.startFS = FingeringState(None, (), 0, False)
        self.prevFSs = [self.startFS]

        self.allFSs = [self.startFS]

    def generateFingeringStates(self):

        while self.currentSS is not None:

            fss1ForCurrentSS, usedAssignmentsToCurrFSs = self._generateFingeringStates(
                self.prevFSs, self.currentSS, None, False)

            fss2ForCurrentSS = []

            if self.prevSS is not None:

                fssForSubstitution = self._generateFingeringStates(
                    self.prevFSs, self.prevSS, None, True)[0]

                fss2ForCurrentSS = self._generateFingeringStates(
                    fssForSubstitution, self.currentSS, usedAssignmentsToCurrFSs, False)[0]

            self.prevFSs = fss1ForCurrentSS + fss2ForCurrentSS

            self.prevSS = self.currentSS
            self.currentSS = self.currentSS.next

        goalFS = FingeringState(None, (), 0, False)
        for prevFS in self.prevFSs:
            prevFS.children.append((goalFS, 0))
        self.allFSs.append(goalFS)

        return self.allFSs

    def _generateFingeringStates(self, prevFSs, currentSS, usedAssignmentsToFS, substitution):

        currPitches = currentSS.getPitches()
        if self.prevSS is not None:
            prevPitches = self.prevSS.getPitches()
        else:
            prevPitches = []

        if usedAssignmentsToFS is None:
            usedAssignmentsToFS = dict()

        fssForCurrentSS = []
        for prevFS in prevFSs:

            availableFingers = self.getUnusedFingersInPrevFS(prevPitches, prevFS, currPitches)

            # Currently, we don't support the case of crossed fingers in an assignment for a
            # single score state, and thus all candidate assignments generated are in finger
            # order. (We of course support the case of crossed fingers from one score state
            # to the next.
            assignments = list(combinations(availableFingers, len(currPitches)))

            heldPitches = currentSS.getHeldPitches()
            if not substitution:
                self.adjustHeldPitchesForVoicing(prevPitches, heldPitches, currPitches)

            self.removeInvalidAssignments(
                prevFS, heldPitches, currPitches, assignments, substitution)

            for a in assignments:

                if prevFS.scoreState is None:
                    horizCost = 0.0
                else:
                    horizCost = getHorizCost(prevPitches, prevFS.assignment, currPitches, a)

                if horizCost == float('inf'):
                    continue
                if substitution:
                    horizCost += substitutionCost

                if a in usedAssignmentsToFS:
                    fs = usedAssignmentsToFS[a]
                    child = (fs, horizCost)
                else:
                    vertCost = getVertCost(currPitches, a)

                    if vertCost == float('inf'):
                        continue

                    fs = FingeringState(currentSS, a, vertCost, substitution)
                    child = (fs, horizCost)

                    usedAssignmentsToFS[a] = fs
                    fssForCurrentSS.append(fs)
                    self.allFSs.append(fs)

                prevFS.children.append(child)

        return fssForCurrentSS, usedAssignmentsToFS

    def getUnusedFingersInPrevFS(self, prevPitches, prevFS, currPitches):

        availableFingers = [1, 2, 3, 4, 5]
        for f in prevFS.assignment:
            availableFingers.remove(f)
        for prevP in prevPitches:
            if prevP in currPitches:
                assert prevFS.getFingerByPitch(prevP) not in availableFingers
                availableFingers.append(prevFS.getFingerByPitch(prevP))
        return sorted(availableFingers)

    def adjustHeldPitchesForVoicing(self, prevPitches, heldPitches, currPitches):

        for p in currPitches:
            if self.isSopranoToAltoExchange(p, currPitches, prevPitches):
                if p not in heldPitches:
                    heldPitches.append(p)
                    heldPitches.sort()
            if self.isAltoToSopranoExchange(p, currPitches, prevPitches):
                if p in heldPitches:
                    heldPitches.remove(p)

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

    def removeInvalidAssignments(self, prevFS, heldPitches, currPitches, assignments, substitution):

        toRemove = set()
        for a in assignments:

            if (not substitution and
                self.isInvalidAssignmentForHeldPitch(prevFS, heldPitches, currPitches, a)):

                toRemove.add(a)

        for a in toRemove:
            assignments.remove(a)

    def isInvalidAssignmentForHeldPitch(self, prevFS, heldPitches, currPitches, assignment):

        for p in heldPitches:
            fingerAssignedToHeldPitch = assignment[currPitches.index(p)]
            fingerThatPressedHeldPitch = prevFS.getFingerByPitch(p)
            if fingerAssignedToHeldPitch != fingerThatPressedHeldPitch:
                return True
        return False