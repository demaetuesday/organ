from os.path import expanduser
from music21 import converter
from scorestates import *
from src.fingeringstates import *
from output import *


score = converter.parse('scores/amfiog.xml')
#score = converter.parse('scores/rest_test.xml')
#score = converter.parse('scores/monophony_test.xml')
#score = converter.parse('scores/triad_test.xml')

print "Parts:"
for p in score.parts:
    print p

#score.show()

rh = score.parts[0]

startSS = ScoreStateGenerator(rh, 2).generateScoreStates()

currentSS = startSS
counter = 0
while currentSS is not None:
    print currentSS.toString()
    counter += 1
    currentSS = currentSS.next
print 'Score states: ' + str(counter)
print

allFS = FingeringStateGenerator(startSS).generateFingeringStates()

for fs in allFS:
    print fs.toString()
    print

toDotGraph(allFS, expanduser('~') + '/Desktop/graph.txt')