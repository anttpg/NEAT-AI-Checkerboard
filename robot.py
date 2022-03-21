import random

class robot:
    color = ""
    currentState = []
    name = -1
    choiceFrom = [-1,-1,-1]
    choiceTo = [-1,0,0]
    fitness = 0


    def __init__(self,c,data,n):
        self.color = c
        self.currentState = data
        self.name = n

    def giveData(self,data): ##sets the current state of the board 
        self.currentState = data

    def changeFitness(self,f):
        self.fitness += f

    def getFitness(self):
        return self.fitness
        
    def resetFitness(self):
        self.fitness = 0


    def resetChoice(self): ##called at the end of each turn.
        self.choiceFrom = [-1,-1,-1]
        self.choiceTo = [-1,0,0]

    def setSelection(self,cF,cT):
        self.choiceFrom = cF
        self.choiceTo = cT
        
        
    def isRobot(self):
        return True



    def getOriginalChecker(self):
        return self.choiceFrom
        
    def getFinalChecker(self):
        return self.choiceTo

    def getRank(self):
        return self.choiceFrom[0]

    def getMove(self):
        return [self.choiceTo[1],self.choiceTo[2]]

    def getColor(self):
        return self.color

    def getName(self):
        return self.name