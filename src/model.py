class ScoreState(object):

    def __init__(self):

        self.scoreStateNotes = []
        self.next = None

    def append(self, scoreStateNote):

        self.scoreStateNotes.append(scoreStateNote)
        self.scoreStateNotes.sort(key = lambda ssN: ssN.note.pitch.midi)

    def getPitches(self):
        pitches = []
        for ssN in self.scoreStateNotes:
            pitches.append(ssN.note.pitch.midi)
        return sorted(list(set(pitches)))

    def getHeldPitches(self):
        heldPitches = []
        for ssN in self.scoreStateNotes:
            if not ssN.onset:
                heldPitches.append(ssN.note.pitch.midi)
        return sorted(list(set(heldPitches)))

    def toString(self):

        result = ''
        for ssN in self.scoreStateNotes:
            result += str(ssN.note.pitch) + ' ' + str(ssN.onset) + ', '
        return result

class ScoreStateNote(object):

    def __init__(self, n, onset):

        self.note = n
        self.onset = onset

class FingeringState(object):

    idCounter = 0

    def __init__(self, scoreState, fingers, vertCost):

        self.id = FingeringState.idCounter
        FingeringState.idCounter += 1

        self.scoreState = scoreState
        self.fingers = fingers
        self.vertCost = vertCost
        self.children = []

    def getFingerByPitch(self, pitch):
        return self.fingers[self.scoreState.getPitches().index(pitch)]

    def toString(self):

        scoreStateString = 'No score state'
        if self.scoreState is not None:
            scoreStateString = self.scoreState.toString()

        result = 'ID: ' + str(self.id) + '\n'
        result += scoreStateString + '\n'
        result += str(self.fingers) + '\n'
        result += 'Vertical cost: ' + str(self.vertCost)
        return result