from fingeringgenerator import *
from evaluator import *
from os.path import expanduser

#score = converter.parse('scores/hyfrydol.xml')
#score = converter.parse('scores/lobe_den_herren.xml')
#score = converter.parse('scores/from_lyra_davidica.xml')

fg = FingeringGenerator()

# fingering = fg.generateFingering('scores/hyfrydol.xml', 1, 4)
# fingering = fg.generateFingering('scores/hyfrydol.xml', 1, 8)
# fingering = fg.generateFingering('scores/lobe_den_herren.xml', 1, 6)
fingering = fg.generateFingering('scores/from_lyra_davidica.xml', 1, 2)
# fingering = fg.generateFingering('scores/from_lyra_davidica.xml', 15, 16)

fg.writeDotGraph(expanduser('~') + '/Desktop/graph.txt')

print 'Fingering:'
print
print fg.toString()
print

# refFingeringPath = 'references/hyfrydol1-4.txt'
# refFingeringPath = 'references/hyfrydol1-8.txt'
# refFingeringPath = 'references/lobe_den_herren1-6.txt'
refFingeringPath = 'references/from_lyra_davidica1-2.txt'
# refFingeringPath = 'references/from_lyra_davidica15-16.txt'

ev = Evaluator()
score, trace = ev.evaluate(fingering, refFingeringPath)

print 'Evaluation:'
print
print 'Score: ' + str(score)
print
print trace