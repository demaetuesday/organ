from music21 import stream, note
from model import *

class ScoreStateGenerator(object):

    def __init__(self, score, measureLimit):

        self.score = score
        self.measureLimit = measureLimit

    def generateScoreStates(self):

        measure1 = self.score.measure(1)
        barDuration = measure1.barDuration.quarterLength

        RHNotes = stream.Stream()
        for e in self.score.flat.elements:
            if isinstance(e, note.Note):
                RHNotes.append(e)

        currentTime = 1.0
        startSS = ScoreState()
        currentSS = startSS
        noteRemainingDuration = dict()

        for n in RHNotes:

            # Currently, assumes that notes in RHNotes are ordered with
            # monotonically increasing noteTime values.

            # Makeshift mechanism to select only the first n beats
            #if self.getNoteTime(n, barDuration) == 4:
                #break

            if (self.measureLimit is not None and
                self.getNoteTime(n, barDuration) >= self.measureLimit * barDuration + 1):

                break

            noteTime = self.getNoteTime(n, barDuration)

            if noteTime == currentTime:
                currentSS.append(ScoreStateNote(n, True))
            else:
                timeAdvancement = noteTime - currentTime
                currentTime = noteTime
                prevSS = currentSS
                currentSS = ScoreState()
                prevSS.next = currentSS
                currentSS.append(ScoreStateNote(n, True))

                for k in noteRemainingDuration:
                    noteRemainingDuration[k] -= timeAdvancement
                    if noteRemainingDuration[k] > 0.0:
                        currentSS.append(ScoreStateNote(k, False))

            noteRemainingDuration[n] = n.duration.quarterLength

        return startSS

    def getNoteTime(self, note, barDuration):

        return (note.measureNumber - 1) * barDuration + note.beat