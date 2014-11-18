from music21 import stream, note
from model import *

class ScoreStateGenerator(object):

    def __init__(self, score, startMeasure, endMeasure):

        self.score = score
        self.startMeasure = startMeasure
        self.endMeasure = endMeasure

    def generateScoreStates(self):

        measure1 = self.score.measure(1)
        barDuration = measure1.barDuration.quarterLength

        RHNotes = stream.Stream()
        for e in self.score.flat.elements:
            if isinstance(e, note.Note):
                RHNotes.append(e)

        currentTime = None
        startSS = ScoreState()
        currentSS = startSS
        noteRemainingDuration = dict()

        for n in RHNotes:

            # Currently, assumes that notes in RHNotes are ordered with
            # monotonically increasing noteTime values.

            if (self.startMeasure is not None and self.endMeasure is not None and
                (self.getNoteTime(n, barDuration) < (self.startMeasure - 1) * barDuration + 1 or
                self.getNoteTime(n, barDuration) >= self.endMeasure * barDuration + 1)):

                continue

            noteTime = self.getNoteTime(n, barDuration)
            if currentTime is None:
                currentTime = noteTime

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