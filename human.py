from tkinter import *
import random

class human:
    color = ""
    currentState = []

    choiceFrom = [-1,-1,-1]
    choiceTo = [-1,0,0]


    def __init__(self,c,data):
        self.color = c
        self.currentState = data

    def giveData(self,data): ##sets the current state of the board 
        self.currentState = data 
    
    def getData(self):
        return self.currentState



    def resetChoice(self): ##called at the end of each turn.
        self.choiceFrom = [-1,-1,-1]
        self.choiceTo = [-1,0,0]
        
    def requestSelection(self): 
        self.choiceFrom = list(map( int, input("[Human] Checker from:")))
        self.choiceTo = list(map( int, input("[Human] Location to:")))

    def isRobot():
        return False


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




 








