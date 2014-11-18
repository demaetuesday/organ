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
#score = converter.parse('scores/lobe_den_herren.xml')
#score = converter.parse('scores/from_lyra_davidica.xml')

# print "Parts:"
# for p in score.parts:
#     print p

#score.show()

rh = score.parts[0]

startSS = ScoreStateGenerator(rh, 1, 3).generateScoreStates()

currentSS = startSS
counter = 0
while currentSS is not None:
    print currentSS.toString()
    counter += 1
    currentSS = currentSS.next
print 'Score states: ' + str(counter)
print

allFSs = FingeringStateGenerator(startSS).generateFingeringStates()

# for fs in allFSs:
#     print fs.toString()
#     print

pathFSs = getShortestPath(allFSs[0], allFSs[-1], allFSs)

toDotGraph(allFSs, pathFSs, expanduser('~') + '/Desktop/graph.txt')

del pathFSs[0]
del pathFSs[-1]

for fs in pathFSs:
    print fs.toString()
    print

print 'Fingering:'
formatStr = '{0: <8}'
for fs in pathFSs:
    if len(fs.fingers) > 1:
        print formatStr.format(fs.fingers[1]),
    else:
        print formatStr.format(''),
print
for fs in pathFSs:
    print formatStr.format(fs.fingers[0]),