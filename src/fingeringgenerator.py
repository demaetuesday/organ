from music21 import converter
from scorestates import *
from fingeringstates import *
from graphs import *
from dotgraph import *

class FingeringGenerator(object):

    def __init__(self):

        self._allFSs = None
        self._fingering = None

    def generateFingering(self, filePath, startMeasure, endMeasure):

        score = converter.parse(filePath)

        # print "Parts:"
        # for p in score.parts:
        #      print p

        #score.show()

        part = score.parts[0]
        # print rh

        startSS = ScoreStateGenerator(part, startMeasure, endMeasure).generateScoreStates()

        # currentSS = startSS
        # counter = 0
        # while currentSS is not None:
        #     print currentSS.toString()
        #     counter += 1
        #     currentSS = currentSS.next
        # print 'Score states: ' + str(counter)
        # print

        self._allFSs = FingeringStateGenerator(startSS).generateFingeringStates()

        # for fs in allFSs:
        #     print fs.toString()
        #     print

        self._fingering = getShortestPath(self._allFSs[0], self._allFSs[-1], self._allFSs)

        result = list(self._fingering)
        del result[0]
        del result[-1]
        return result

    def toString(self):

        fsSequence = list(self._fingering)
        del fsSequence[0]
        del fsSequence[-1]

        result = ''
        formatS = '{0: <8}'
        for fs in fsSequence:
            if len(fs.assignment) > 1:
                result += formatS.format(fs.assignment[1])
            else:
                result += formatS.format('')
        result += '\n'
        for fs in fsSequence:
            result += formatS.format(fs.assignment[0])
        result += '\n'
        for fs in fsSequence:
            if fs.substitution:
                result += formatS.format('Sub')
            else:
                result += formatS.format('')
        return result

    def writeDotGraph(self, filePath):

        toDotGraph(self._allFSs, self._fingering, filePath)
