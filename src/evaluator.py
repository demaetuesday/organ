class Evaluator(object):

    def evaluate(self, fsSequence, filePath):

        hypoth = []
        for fs in fsSequence:
            hypoth.append((fs.assignment, fs.substitution))

        evalFs = self.getEvalFingerings(filePath)

        n = len(hypoth)
        for evalF in evalFs:
            if len(evalF) < n:
                evalF.extend([()] * (n - len(evalF)))

        matches = 0
        for i in range(n):
            match = False
            for evalF in evalFs:
                if hypoth[i][0] == evalF[i][0]:
                    match = True
            if match:
                matches += 1

        score = float(matches) / n

        return score, self.getTrace(hypoth, evalFs)


    def getEvalFingerings(self, filePath):

        evalFs = []
        f = open(filePath)
        lines = f.readlines()
        for line in lines:
            evalF = []
            aStrings = line.split()
            for aString in aStrings:
                evalF.append(self.parseAssignment(aString))
            evalFs.append(evalF)
        return evalFs

    # def align(self, hypoth, refFingerings):
    #
    #     ss = 1
    #     hypothSS = 1
    #     refSS = [1] * len(refFingerings)
    #
    #     done = False
    #     while not done:
    #
    #

    def parseAssignment(self, aString):

        aList = []
        substitution = False
        for c in aString:
            if c == 's':
                substitution = True
            else:
                aList.append(int(c))
        return tuple(aList), substitution

    def getTrace(self, hypoth, evalFs):

        n = len(hypoth)
        formatS = '{0: <10}'

        result = ''
        result += 'Trace:\n\n'

        result += 'Fingering:\n'
        for fs in hypoth:
            if fs[1]:
                result += formatS.format(str(fs[0]) + 'S')
            else:
                result += formatS.format(fs[0])
        result += '\n\n'

        for i in range(len(evalFs)):
            result += 'Evaluation fingering ' + str(i) + ":\n"
            evalF = evalFs[i]
            for j in range(n):
                span = str(evalF[j][0])
                if evalF[j][1]:
                    span += 'S'
                result += formatS.format(span)
            result += '\n'
            for j in range(n):
                if evalF[j][0] == hypoth[j][0]:
                    result += formatS.format('')
                else:
                    result += formatS.format('Diff')
            result += '\n'
        return result