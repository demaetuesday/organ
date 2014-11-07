def toDotGraph(fingeringStates, filename):

    result = 'digraph g {\n'
    result += 'rankdir=LR ranksep=2.0\n'

    for fs in fingeringStates:
        for child in fs.children:

            result += getNodeNameString(fs)
            result += " -> "
            result += getNodeNameString(child[0])
            result += ' [label="' + "{0:.2f}".format(child[1]) + '"]'
            result += ";\n"

    result += "}\n"

    f = open(filename, 'w')
    f.write(result)
    f.close()

def getNodeNameString(fingeringState):

    scoreStateString = 'No score state'
    if fingeringState.scoreState is not None:
        scoreStateString = fingeringState.scoreState.toString()

    result = '\"ID: ' + str(fingeringState.id) + '\\n'
    result += scoreStateString + '\\n'
    result += str(fingeringState.fingers) + '\\n'
    result += 'Vertical cost: ' + str(fingeringState.vertCost) + '\"'
    return result