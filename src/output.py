def toDotGraph(allFSs, pathFSs, filename):

    result = 'digraph g {\n'
    result += 'rankdir=LR ranksep=5.0;\n'
    result += 'node [style=filled fillcolor=white];\n'

    for fs in allFSs:
        result += getNodeNameString(fs)
        if fs in pathFSs:
            result += ' [fillcolor=palegreen]'
        elif fs.substitution:
            result += ' [fillcolor=yellow]'
        result += ';\n'

    pathCounter = 0
    for fs in allFSs:
        for child in fs.children:

            result += getNodeNameString(fs)
            result += " -> "
            result += getNodeNameString(child[0])

            label = ' [label="'
            label += str(fs.assignment)
            if fs.substitution:
                label += 'S'
            label += ' ' + "{0:.2f}".format(child[1]) + ' '
            label += str(child[0].assignment)
            if child[0].substitution:
                label += 'S'
            label += '"'

            result += label
            if fs == pathFSs[pathCounter] and child[0] == pathFSs[pathCounter + 1]:
                result += ' penwidth=5 color=palegreen]'
                pathCounter += 1
            else:
                result += ']'
            result += ';\n'

    result += "}\n"

    f = open(filename, 'w')
    f.write(result)
    f.close()

def getNodeNameString(fingeringState):

    scoreStateString = 'No score state'
    if fingeringState.scoreState is not None:
        scoreStateString = fingeringState.scoreState.toString()

    result = '"' + scoreStateString + '\\n'
    result += str(fingeringState.assignment) + '\\n'
    result += 'Vertical cost: ' + str(fingeringState.vertCost) + '\\n'
    result += 'ID: ' + str(fingeringState.id) + '"'
    return result