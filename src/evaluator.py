class Evaluator(object):

    def evaluate(self, fsSequence, filePath):

        evalFs = self.getEvalFingerings(filePath)

        n = len(fsSequence)
        for evalF in evalFs:
            if len(evalF) < n:
                evalF.extend([()] * (n - len(evalF)))

        matches = 0
        for i in range(n):
            match = False
            for evalF in evalFs:
                if fsSequence[i].assignment == evalF[i][0]:
                    match = True
            if match:
                matches += 1

        score = float(matches) / n

        return score, self.getTrace(fsSequence, evalFs)


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

    def parseAssignment(self, aString):

        aList = []
        substitution = False
        for c in aString:
            if c == 's':
                substitution = True
            else:
                aList.append(int(c))
        return tuple(aList), substitution

    def getTrace(self, fsSequence, evalFs):

        n = len(fsSequence)
        formatS = '{0: <10}'

        result = ''
        result += 'Trace:\n\n'

        result += 'Fingering:\n'
        for fs in fsSequence:
            #result += formatS.format(fs.assignment)
            if fs.substitution:
                result += formatS.format(str(fs.assignment) + 'S')
            else:
                result += formatS.format(fs.assignment)
        # result += '\n'
        # for fs in fsSequence:
        #     if fs.substitution:
        #         result += formatS.format('Sub')
        #     else:
        #         result += formatS.format('')
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
                if evalF[j][0] == fsSequence[j].assignment:
                    result += formatS.format('')
                else:
                    result += formatS.format('Diff')
            result += '\n'
        return result