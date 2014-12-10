from os.path import expanduser
from music21 import converter
from scorestates import *
from fingeringstates import *
from output import *
from graphs import *
from evaluator import *

score = converter.parse('scores/hyfrydol.xml')
#score = converter.parse('scores/from_lyra_davidica.xml')

#score = converter.parse('scores/amfiog.xml')
#score = converter.parse('scores/rest_test.xml')
#score = converter.parse('scores/monophony_test.xml')
#score = converter.parse('scores/triad_test.xml')
#score = converter.parse('scores/lobe_den_herren.xml')
#score = converter.parse('scores/third_test.xml')

# print "Parts:"
# for p in score.parts:
#      print p

#score.show()

rh = score.parts[0]
# print rh

startSS = ScoreStateGenerator(rh, 1, 8).generateScoreStates()

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

fsSequence = getShortestPath(allFSs[0], allFSs[-1], allFSs)

toDotGraph(allFSs, fsSequence, expanduser('~') + '/Desktop/graph.txt')

del fsSequence[0]
del fsSequence[-1]

# for fs in fsSequence:
#     print fs.toString()
#     print

print 'Fingering:'
print
formatS = '{0: <8}'
for fs in fsSequence:
    if len(fs.assignment) > 1:
        print formatS.format(fs.assignment[1]),
    else:
        print formatS.format(''),
print
for fs in fsSequence:
    print formatS.format(fs.assignment[0]),
print
for fs in fsSequence:
    if fs.substitution:
        print formatS.format('Sub'),
    else:
        print formatS.format(''),
print
print

#evalFingeringPath = 'evalfingerings/hyfrydol1-4.txt'
evalFingeringPath = 'evalfingerings/hyfrydol1-8.txt'
#evalFingeringPath = 'evalfingerings/from_lyra_davidica1-2.txt'
#evalFingeringPath = 'evalfingerings/from_lyra_davidica15-16.txt'

ev = Evaluator()
score, trace = ev.evaluate(fsSequence, evalFingeringPath)

print 'Evaluation:'
print
print 'Score: ' + str(score)
print
print trace

