from tkinter import *
import random

from graphicalBoard import GraphicalBoard

class Human:
    choiceFrom = [-1,-1,-1]
    choiceTo = [-1,0,0]
    fitness = 0
    isSelected = False


    def __init__(self,c,data,n):
        self.color = c
        self.currentState = data
        self.name = n

    def giveData(self,data): ##sets the current state of the board 
        self.currentState = data 
    
    def getData(self):
        return self.currentState



    def resetChoice(self): ##called at the end of each turn.
        self.choiceFrom = [-1,-1,-1]
        self.choiceTo = [-1,0,0]

    def setSelection(self,cF,cT):
        self.choiceFrom = [cF[0], cF[1], cF[2]]
        self.choiceTo = [cT[0], cT[1]]
    
    def setChoice(self, cF):
        self.choiceFrom = [cF[0], cF[2], cF[1]]

    def setMove(self,cF):
        self.choiceTo = [self.choiceFrom[0], cF[0], cF[1]]


    def isRobot(self):
        return False



    def changeFitness(self,f):
        self.fitness += f

    def getFitness(self):
        return self.fitness
        
    def resetFitness(self):
        self.fitness = 0



    def getOriginalChecker(self):
        return self.choiceFrom


    def getPosition(self):
        return self.choiceFrom
        

    def getFinalChecker(self):
        return [self.choiceTo[0], self.choiceTo[2], self.choiceTo[1]]

    def getRank(self):
        return self.choiceFrom[0]

    def getMove(self):
        return [self.choiceTo[2], self.choiceTo[1]]

    def getColor(self):
        return self.color




 








