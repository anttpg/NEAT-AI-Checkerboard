from sys import builtin_module_names
import random as rand
from copy import copy
from Robot import *
from Human import *

class checkerboardClass:
    data = []
    currentTurn = "Blue"
    makeKing = False
    win = False
    turnTimer = 0

    ##sets up who will be playing what and board configuration
    def __init__(self, boardConfig, red, blue, p1, p2):
        self.board = boardConfig
        self.redCheckers = red
        self.blueCheckers = blue
        self.p1 = p1
        self.p2 = p2

    def getTurn(self):
        return self.turnTimer
    

    def reset(self):
        self.p1.resetChoice()
        self.p2.resetChoice()
        self.p1.resetFitness()
        self.p2.resetFitness()
        

        
        
    def refreshData(self):
        tempC = []
        
        for i in range(len(self.redCheckers)):
            strng = [str(red) for red in self.redCheckers[i]]
            #strng.append(str(rand.randint(0,9)))
            a_string = "".join(strng)
            if(a_string != '-2-2-2'):
                final = ((int(a_string))/1000)
            else:
                final = 0.75
            #CONVERTS IE 1359 (KING,Y,X,COLOR) to 1.359 for activation - 2 so that Gauss can properly work

            tempC.append(final)
            tempC.append(1) # REPRESENTS RED
            


        for i in range(len(self.blueCheckers)):
            strng = [str(blue) for blue in self.blueCheckers[i]]
            
            #strng.append(str(rand.randint(0,9)))
            
            a_string = "".join(strng)
            if(a_string != '-2-2-2'):
                final = ((int(a_string))/1000)
            else:
                final = 0.25
            #CONVERTS IE 1359 (KING,Y,X,COLOR) to 1.359 for activation - 2 so that Gauss can properly work
            
            tempC.append(final)
            tempC.append(0.5) # REPRESENTS BLUE

        self.data = tempC
        return tempC


    def getData(self):
        return self.data

    

    def getSelection(self,p,netsOutput):
        moveList = []
        move = [0,0,0]
        originalChecker = []
        tempC = [1,-10,-10]
        

        if self.currentTurn == "Blue":
            legalJumps = [[1,1],[2,2],[1,-1],[2,-2],[-1,-1],[-2,-2],[-1,1],[-2,2]]
        else:
            legalJumps = [[-1,-1],[-2,-2],[-1,1],[-2,2],[1,1],[2,2],[1,-1],[2,-2]] 

        for y in range(8):
            for x in range(8):
                if y % 2 == x % 2:
                    if self.legalChoice([1,y+1,x+1],self.currentTurn):
                        originalChecker = [1,y+1,x+1]
                        move[0] = 1

                    elif self.legalChoice([2,y+1,x+1],self.currentTurn):
                        originalChecker = [2,y+1,x+1]
                        move[0] = 2
                    else:
                        continue
                    
                    

                    for i in range(4 * originalChecker[0]):
                        ##IE [1,(3+1),(5+1)]
                        tempC[1] = originalChecker[1] + legalJumps[i][0]
                        tempC[2] = originalChecker[2] + legalJumps[i][1]
                        move[1] = originalChecker[1] + legalJumps[i][0]
                        move[2] = originalChecker[2] + legalJumps[i][1]
                        ##getMove() returns the move position IE [4,6]
                        #print(tempC)
                        if((move[1]!=0 and move[1]!=9) and 
                            (move[2]!=0 and move[2]!=9)):
                            ##Makes sure place chosen is free to prevent jumping on another checker
                            if(not(  self.legalChoice( tempC, "Blue") or self.legalChoice( [2,tempC[1],tempC[2]], "Blue") 
                                or self.legalChoice( tempC, "Red" ) or self.legalChoice( [2,tempC[1],tempC[2]], "Red" )  )):

                                ##checks if its a jump move
                                if(i % 2 == 1):
                                    capturedChecker = None
                                    try:
                                        if(self.currentTurn == "Blue"):
                                            capturedChecker = self.redCheckers.index([  1, move[1]-legalJumps[i-1][0], move[2]-legalJumps[i-1][1]  ])
                                            
                                        else:
                                            capturedChecker = self.blueCheckers.index([  1, move[1]-legalJumps[i-1][0], move[2]-legalJumps[i-1][1]  ])
                                        moveList.append([originalChecker,copy(move)])
                                        moveList.append([originalChecker,copy(move)])
                                        moveList.append([originalChecker,copy(move)])
                                    except:
                                        pass
                                        

                                    if(capturedChecker == None): 
                                        try:
                                            if(self.currentTurn == "Blue"):
                                                capturedChecker = self.redCheckers.index([  2, move[1]-legalJumps[i-1][0], move[2]-legalJumps[i-1][1]  ])
                                                
                                            else:
                                                capturedChecker = self.blueCheckers.index([  2, move[1]-legalJumps[i-1][0], move[2]-legalJumps[i-1][1]  ])
                                            moveList.append([originalChecker,copy(move)])
                                            moveList.append([originalChecker,copy(move)])
                                            moveList.append([originalChecker,copy(move)])
                                        except:
                                            pass
                                            ##means there was no checker to jump. Return failed input
                                    

                                ##else just a normal move    
                                else:
                                    moveList.append([originalChecker,copy(move)])
        
        
        o = round(len(moveList)*((netsOutput[0] + netsOutput[1] + netsOutput[2] + netsOutput[3])/4))
        if (len(moveList) == o):
            o = o-1
        if(moveList == []):
            self.win = True
            return
        p.setSelection(moveList[o][0], moveList[o][1]) 
       


    
    def prettyBoard(self):
        for y in range(8):
            for x in range(8):
                if y % 2 == x % 2:
                    if self.legalChoice([1,y+1,x+1],"Blue"):
                        self.board[y][x] = "b"
                    elif self.legalChoice([2,y+1,x+1],"Blue"):
                        self.board[y][x] = "B" 
                    elif self.legalChoice([1,y+1,x+1],"Red"):
                        self.board[y][x] = "r"
                    elif self.legalChoice([2,y+1,x+1],"Red"):
                        self.board[y][x] = "R"
                    else:
                        self.board[y][x] = "_"

                else:                   
                    self.board[y][x] = "#"

            print(self.board[y][0],self.board[y][1],self.board[y][2],self.board[y][3],
                  self.board[y][4],self.board[y][5],self.board[y][6],self.board[y][7])
        
        print('')
            
        



   
                

    ## move format should be [[checker, x, y]]
    def turn(self,p):
        #p.requestSelection()
        #print("selection made!")
        #print(p.getOriginalChecker())

        if self.legalChoice(p.getOriginalChecker(),p.getColor()): ##made for multi step moves, will run through recursion
            #print("choice is legal!")
            if(self.legalMove(p)): ##moving is built in to checking if it is legal
                #print("move is legal!")
                self.makeKing = False
                if(not self.redCheckers):
                    self.win = True
                    self.p1.changeFitness(5)
                if(not self.blueCheckers):
                    self.win = True
                    self.p2.changeFitness(5)
                
                p.giveData([self.redCheckers,self.blueCheckers])
                self.switchTurn()
                self.turnTimer += 1
            
        else:
            print("Sorry! That is not a legal move. Please follow the 135 format, [Rank + Y + X].")
            #p.changeFitness(-1)
        p.resetChoice()
        
        


                ## TODO if(self.legalMove(p.getMove())): ##if another move is possible from the new position...
                    ##call for input move...
                    #
                    ##then run again with recursion.
                    



    ##Called so that checker chosen has to be a valid option
    def legalChoice(self,choice,color):
        if color == "Blue":
            if(choice in self.blueCheckers):
                return True    

        elif (choice in self.redCheckers):             
            return True
        
        return False



    def switchTurn(self):
        if(self.currentTurn == "Blue"):
           self.currentTurn = "Red"
        else:
            self.currentTurn = "Blue"



    def makeMove(self, p, jump, capturedChecker):
        if(p.getColor() == "Blue"):
            self.blueCheckers[self.blueCheckers.index(p.getOriginalChecker())] = p.getFinalChecker() ##updates new checker position

            if(jump):
                self.redCheckers[capturedChecker] = [-2,-2,-2]
                if(p.isRobot()):
                    p.changeFitness(1)  ## good move means robot fitness increases

            if(self.makeKing == True):
                self.blueCheckers[self.blueCheckers.index(p.getFinalChecker())][0] = 2
                if(p.isRobot()):
                    p.changeFitness(2)

    
        else:
            self.redCheckers[self.redCheckers.index(p.getOriginalChecker())] = p.getFinalChecker()

            if(jump):
                self.blueCheckers[capturedChecker] = [-2,-2,-2]
                if(p.isRobot()):
                    p.changeFitness(1)
                    

            if(self.makeKing == True):
                self.redCheckers[self.redCheckers.index(p.getFinalChecker())][0] = 2
                if(p.isRobot()):
                    p.changeFitness(2)
        


    def getJumpedChecker(self,rank,p,legalJumps,i):
        return([  rank, p.getMove()[0]-legalJumps[i-1][0], p.getMove()[1]-legalJumps[i-1][1]  ])


    ## move format should be [[rank, y, x]]
    def legalMove(self,p):
        tempC = [1,-10,-10]
        if p.getColor() == "Blue":
            legalJumps = [[1,1],[2,2],[1,-1],[2,-2],[-1,-1],[-2,-2],[-1,1],[-2,2]]
        else:
            legalJumps = [[-1,-1],[-2,-2],[-1,1],[-2,2],[1,1],[2,2],[1,-1],[2,-2]]
        
        ##(int)((len(legalJumps)/2)
        for i in range( 4 * p.getRank() ): 
            ##IE [1,(3+1),(5+1)]
            tempC[1] = p.getOriginalChecker()[1] + legalJumps[i][0]
            tempC[2] = p.getOriginalChecker()[2] + legalJumps[i][1]

            ##getMove() returns the move position IE [4,6]
            #print(tempC)
            if((p.getMove() == [tempC[1],tempC[2]]) and 
            (p.getMove()[1]!=0 and p.getMove()[1]!=9) and 
            (p.getMove()[0]!=0 and p.getMove()[0]!=9)):
                if((tempC[1] == 8 and self.currentTurn == "Blue") or (tempC[1] == 1 and self.currentTurn == "Red")):
                    self.makeKing = True
                ##Makes sure place chosen is free to prevent jumping on another checker
                if(not(  self.legalChoice( tempC, "Blue") or self.legalChoice( [2,tempC[1],tempC[2]], "Blue") 
                     or self.legalChoice( tempC, "Red" ) or self.legalChoice( [2,tempC[1],tempC[2]], "Red" )  )):

                    ##checks if its a jump move
                    if(i % 2 == 1):
                        capturedChecker = None
                        try:
                            if(self.currentTurn == "Blue"):
                                capturedChecker = self.redCheckers.index( self.getJumpedChecker(1,p,legalJumps,i) )
                            else:
                                capturedChecker = self.blueCheckers.index( self.getJumpedChecker(1,p,legalJumps,i) )
                            #print(capturedChecker)
                        except:
                            pass
                            

                        if(capturedChecker == None): 
                            try:
                                if(self.currentTurn == "Blue"):
                                    capturedChecker = self.redCheckers.index( self.getJumpedChecker(2,p,legalJumps,i) )
                                else:
                                    capturedChecker = self.blueCheckers.index( self.getJumpedChecker(2,p,legalJumps,i) )
                                #print(capturedChecker)
                            except ValueError:
                                raise ValueError("Could not find checker to jump.") from None
                                return False ##means there was no checker to jump. Return failed input
    
                        self.makeMove(p, True, capturedChecker)
                        #print("captured checker " + str(capturedChecker) + "! moved checker to " + str(p.getMove()) + "!") 
                        return True   

                    ##else just a normal move    
                    else:
                        self.makeMove(p, False, -1)
                        #print("moved checker to " + str(p.getMove()[0]) + str(p.getMove()[1]) + "!")
                        return True 

        return False
                        
                        

