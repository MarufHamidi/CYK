#!/usr/bin/python

def getGrammar(fileName):
    rules = []
    inputFile = open(fileName)
    while True:
        rule = inputFile.readline().strip()
        if len(rule) == 0:
            break
        rules.append(rule)
    inputFile.close()
    #string = rules.pop()
    return rules

def getStrings(fileName):
    strings = []
    inputFile = open(fileName)
    while True:
        string = inputFile.readline().strip()
        if len(string) == 0:
            break
        strings.append(string)
    inputFile.close()
    return strings

def checkCNF(rules):
    grammar = []
    for i in range(0, len(rules)):
        temp = []
        if rules[i].find("->") != 1:
            return False, None
        if rules[i][0] < 'A' or rules[i][0] > 'Z':
            return False, None
        temp.append(rules[i][0])

        rhs = rules[i][3:]    
        p = rhs.split("|")
        for j in range(0, len(p)):
            if len(p[j]) > 2:
                return False, None
            elif len(p[j]) == 1 and (p[j][0] <"a" or p[j][0]>"z"):
                return False, None
            elif len(p[j]) == 2 and ((p[j][0] <"A" or p[j][0]>"Z") or (p[j][1] <"A" or p[j][1]>"Z")):
                return False, None
            temp.append(p[j])
        grammar.append(temp)
    return True, grammar

# merges two strings
def merge(a, b):
    if a.find(b) < 0:
        a = a + b
    return a
    
def initMatrix(rules, string):
    matrix = []
    temp = []
    for i in range(0, len(string)):
        r = ""
        for j in range(0, len(rules)):            
            for k in range(1, len(rules[j])):  
                if string[i] == rules[j][k]:
                    r = merge(r,rules[j][0])
        temp.append(r)
    matrix.append(temp)
    return matrix

def buildMatrix(matrix, rules, string):
    for i in range(1, len(string)):
        temp = []
        for j in range(0, len(string)-i):
            combinations = []
            
            # build combinatins
            for k,l in zip(range(0, i), range(1, len(string))):
                #print "{} {} >{} {}".format(k, j, i-l, j+l)
                if matrix[k][j] == "":
                    combinations.append(matrix[i-l][j+l])
                    #break
                elif matrix[i-l][j+l] == "":
                    combinations.append(matrix[k][j])
                    #break
                
                matrixContent = ""
                for m in range(0, len(matrix[k][j])):
                    for n in range(0, len(matrix[i-l][j+l])):
                        matrixContent = matrix[k][j][m] + matrix[i-l][j+l][n]
                        combinations.append(matrixContent)
            #print combinations
            
            # check each combinations to match any production rule            
            r = ""
            for x in range(0, len(combinations)):                
                for y in range(0, len(rules)):
                    for z in range(1, len(rules[y])):
                        if combinations[x] == rules[y][z]:
                            r = merge(r,rules[y][0])
                            break
            #print r
            temp.append(r)
        matrix.append(temp)
        
    matrix.reverse()
    return matrix

def printMatrix(matrix):
    for i in range(0, len(matrix)):
        print matrix[i]
    

# whether the string can be generated by the given grammar
def decide(matrix, string):
    if matrix[0][0].find("S") >= 0:
        print "{}\t\t>>>\t\tYes".format(string)
    else:
        print "{}\t\t>>>\t\tNo".format(string)

def run():
    rules = getGrammar("grammar.txt")
    strings = getStrings("strings.txt")
    isCnf, rules  = checkCNF(rules)

    for i in range(0, len(strings)):
        matrix = initMatrix(rules, strings[i])
        matrix = buildMatrix(matrix, rules, strings[i])    
        #printMatrix(matrix)
        decide(matrix, strings[i])

run()
