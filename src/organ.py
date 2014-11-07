from os.path import expanduser
from music21 import converter
from scorestates import *
from fingeringstates import *
from output import *
from graphs import *

#score = converter.parse('scores/amfiog.xml')
#score = converter.parse('scores/rest_test.xml')
#score = converter.parse('scores/monophony_test.xml')
#score = converter.parse('scores/triad_test.xml')
score = converter.parse('scores/hyfrydol.xml')

# print "Parts:"
# for p in score.parts:
#     print p

#score.show()

rh = score.parts[0]

startSS = ScoreStateGenerator(rh, 128).generateScoreStates()

# currentSS = startSS
# counter = 0
# while currentSS is not None:
#     print currentSS.toString()
#     counter += 1
#     currentSS = currentSS.next
# print 'Score states: ' + str(counter)
# print

allFSs = FingeringStateGenerator(startSS).generateFingeringStates()

# for fs in allFSs:
#     print fs.toString()
#     print

toDotGraph(allFSs, expanduser('~') + '/Desktop/graph.txt')

fingering = getShortestPath(allFSs[0], allFSs[-1], allFSs)

for fs in fingering:
    print fs.toString()
    print