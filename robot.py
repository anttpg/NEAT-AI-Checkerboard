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
        name = n

    def giveData(self,data): ##sets the current state of the board 
        self.currentState = data

    def changeFitness(self,f):
        self.fitness += f

    def getFitness(self):
        return self.fitness

    # def getData(self):
    #     tempC = []
    #     for i in range(len(self.currentState[0])):
    #         self.currentState[0][i].append(-3)
    #         tempC.append(self.currentState[0][i])

    #     for i in range(len(self.currentState[1])):
    #         self.currentState[1][i].append(-4)
    #         tempC.append(self.currentState[1][i])
    #     tempC.ravel()
    #     return tempC

    def resetChoice(self): ##called at the end of each turn.
        self.choiceFrom = [-1,-1,-1]
        self.choiceTo = [-1,0,0]

    def setSelection(self,cF,cT):
        self.choiceFrom = cF
        self.choiceTo = cT
        
    # def requestSelection(self, f1, f2, t1, t2): 
    #     if(self.color == "Red"):
    #         if([1,f1,f2] in self.currentState[0]):
    #             self.choiceFrom = [1,f1,f2]
    #             self.choiceTo = [1,t1,t2]
    #         elif([2,f1,f2] in self.currentState[0]):
    #             self.choiceFrom = [2,f1,f2]
    #             self.choiceTo = [2,t1,t2]

    #     if(self.color == "Blue"):
    #         if([1,f1,f2] in self.currentState[1]):
    #             self.choiceFrom = [1,f1,f2]
    #             self.choiceTo = [1,t1,t2]
    #         elif([2,f1,f2] in self.currentState[1]):
    #             self.choiceFrom = [2,f1,f2]
    #             self.choiceTo = [2,t1,t2]

    

        
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