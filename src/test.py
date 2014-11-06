from itertools import *
from music21.note import Note
from fingeringstates import *

fsg = FingeringStateGenerator(None)
#print fsg.getHorizCost([10,30,60], (1,3,5), [20,40,60], (1,3,5))
#print fsg.getHorizCost([60,64,67], (1,3,5), [62,65], (2,4))
print fsg.getHorizCost([60,64], (1,5), [62,65], (2,4))
#print fsg.getHorizCost([10,30,50], (1,3,5), [20,40,50], (2,4,5))