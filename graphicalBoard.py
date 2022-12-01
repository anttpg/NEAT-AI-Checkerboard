import copy
import time
from tkinter import *
from threading import Thread



def getXY(row,col,h):
    x=(h/8)*row-(h/8)
    y=(h/8)*col-(h/8)
    
    return (x,y) 

def getStarPoints(x,y,h):
    points= [100,10,45,198,190,74,15,74,160,198]
    for i in range(len(points)):
        points[i] = (points[i]/255*(h/8))+7
        if points[i] % 2 == 0:
            points[i] += y
        else:
            points[i] += x
    return points

#Gets the size of the screen being used.
def get_display_size():
    root = Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    height = root.winfo_screenheight()
    root.destroy()

    #setup so that it works well with all screens. rn -400 is good for me, but doesnt work on a laptop
    #lower priority fix.
    return height-250 #Arbitrary number to make height GUI smaller than screen


class GraphicalBoard:
    mainBoard = None

    initial = []
    spaceID = []
    redObjects = []
    blueObjects = []
    canvas = None
    checker = None
    deleteChecker = None
    display_size = None
    checkerI = 0

    toChange = None
    toDelete = None
    
    

    def __init__(self, mainBoard, human, bestNet):
        self.display_size = get_display_size()
        self.mainBoard = mainBoard
        self.human = human
        self.net = bestNet
        self.turn = "Blue"
        self.initial = [
            [[1,1,1],[1,1,3],[1,1,5],[1,1,7],
            [1,2,2],[1,2,4],[1,2,6],[1,2,8],
            [1,3,1],[1,3,3],[1,3,5],[1,3,7]],[

            [1,6,2],[1,6,4],[1,6,6],[1,6,8],
            [1,7,1],[1,7,3],[1,7,5],[1,7,7],
            [1,8,2],[1,8,4],[1,8,6],[1,8,8]]]
        
        self.boardthread = None

    def start(self):
        self.boardthread = Thread(target=self.boardWindow()).start()

    #Grapics; self explanitory
    def ring(self,w):    
        if self.checker != None:
            self.canvas.itemconfig(self.checker[3], outline='gold',width = w)   

    def hasPlayerMoved(self):
        if(self.human.isSelected == True):
            return True
    
    def setTurn(self, t):
        self.turn = t 

    #Draws the current state of the checkers in a given list
    def draw_checkers(self,tokenList,color):  
        #star = -999
        h=self.display_size
        objects=[]
        for i in range(len(tokenList)):
            rank, col, row = tokenList[i][0],tokenList[i][1],tokenList[i][2]
            x,y = getXY(row,col,h)
            tokenID = self.canvas.create_oval(x,y,x+h/8,y+h/8,fill=color)
            #if rank == 2:
                #points = getStarPoints(x,y,h)
                #star = self.canvas.create_polygon(points,outline="gold",fill="gold",width=4)
            objects.append([rank,row,col,tokenID,color])


        return objects


    #Draw_spaces creates and returns an complete list of the BLACK spaces (white space not important atm). 
    #Includes the position of the spaces, and their ID value
    def draw_spaces(self):
        h=self.display_size
        j=0
        for col in range(8):
            for row in range(8):
                xPos=(h/8)*row
                yPos=(h/8)*col
                if (row+col)%2==1:
                    color = "white"
                else:
                    color = "black"
                space = self.canvas.create_rectangle(xPos,yPos,xPos+h/8,yPos+h/8,fill=color)
                if color == "black":
                    self.spaceID.append([row+1,col+1,space])
                    
        



    def setup(self):
        #legal = False
        self.canvas.delete("all")
        self.draw_spaces()

        self.blueObjects = self.draw_checkers(self.initial[0],"Blue")
        self.redObjects = self.draw_checkers(self.initial[1],"Red")
        del self.initial
               

    def on_click(self, event):
        if(self.mainBoard.currentTurn == self.human.getColor()):
            self.ring(0)
            #Find clicked object
            clickedObject = self.canvas.find_closest(event.x, event.y)[0]
            self.play(clickedObject) ## check to move human






    
    def play(self,clickedObject):
        clickID = clickedObject
        
        for i in range(len(self.blueObjects)):
            if self.blueObjects[i][3] == clickID and self.turn == "Blue":
                self.checker = self.blueObjects[i]
                self.checkerI = i
                self.ring(10)        

        for i in range(len(self.redObjects)):
            if self.redObjects[i][3] == clickID and self.turn == "Red":
                self.checker = self.redObjects[i]
                self.checkerI = i
                self.ring(10)

        for i in range(len(self.spaceID)):
            #if clicked object is a space
            if self.spaceID[i][2] == clickID and self.checker != None:
                if self.legalMove(self.spaceID[i]):
                    self.moveChecker(self.spaceID[i])
                    self.playMainBoard()


    def updateAImoved(self, checker):
        checkerToChange = checker.getOriginalSwapped()
        captured = self.mainBoard.captured

        for red in self.redObjects:
            if(checker.getColor() == "Red" and red[0] == checkerToChange[0] and red[1] == checkerToChange[1] and red[2] == checkerToChange[2]):
                self.toChange = red

            if(captured != None and red[0] == captured[0] and red[1] == captured[1] and red[2] == captured[2] ):
                self.toDelete = copy(captured)

        for blue in self.blueObjects:
            if(checker.getColor() == "Blue" and blue[0] == checkerToChange[0] and blue[1] == checkerToChange[1] and blue[2] == checkerToChange[2]):
                self.toChange = blue

            if(captured != None and blue[0] == captured[0] and blue[1] == captured[1] and blue[2] == captured[2]):
                self.toDelete = copy(captured)

        self.checker = [self.toChange[0], self.toChange[2], self.toChange[1], self.toChange[3], self.toChange[4]]
        self.toChange = self.checker
        self.mainBoard.captured = None


    def removeCaptured(self):
        captured = self.mainBoard.captured

        for i, red in enumerate(self.redObjects):
            if(captured != None and red[0] == captured[0] and red[2] == captured[1] and red[1] == captured[2] ):
                self.toDelete = captured
                self.canvas.delete(red[3])
                self.blueObjects.pop(i)
                break

        for i, blue in enumerate(self.blueObjects):
            if(captured != None and blue[0] == captured[0] and blue[2] == captured[1] and blue[1] == captured[2]):
                self.toDelete = captured
                self.canvas.delete(blue[3])
                self.blueObjects.pop(i)
                break
                
        self.mainBoard.captured = None



                                    
    def playMainBoard(self):
        if(self.mainBoard.win == False):
            if (self.mainBoard.currentTurn == "Blue"):
                if(self.mainBoard.p1.isRobot()):
                    output = self.net.activate(self.mainBoard.refreshData()) 
                    self.mainBoard.getSelection(self.mainBoard.p1,output) 

                    self.removeCaptured()
                    self.updateAImoved(self.mainBoard.p1)
                    self.legalMove(self.mainBoard.p1.getMoveSwapped())

                    for i in range(len(self.spaceID)):
                        if(self.spaceID[i][0] == self.mainBoard.p1.getMoveSwapped()[0] and self.spaceID[i][1] == self.mainBoard.p1.getMoveSwapped()[1]):
                            self.checker = self.toChange
                            self.moveChecker(self.spaceID[i])
                            #print("blue computer has moved from " + ','.join(self.mainBoard.p1.getOriginalChecker()) + " to " + ','.join(self.mainBoard.p1.getMoveSwapped()))

                else:
                    print("blue player has moved") 


                if(self.mainBoard.win == False and self.mainBoard.turnTimer < 125):
                    self.mainBoard.turn(self.mainBoard.p1)
                    if(not self.mainBoard.p1.isRobot()):
                        self.playMainBoard()
                        self.removeCaptured()
                else:
                    self.mainBoard.p2.changeFitness(15)   

            
            else: # must be red
                if(self.mainBoard.p2.isRobot()):
                    time.sleep(0.5)
                    output = self.net.activate(self.mainBoard.refreshData()) ##Red checkers, blue checkers. BLUE CHECKER ROBOT
                    self.mainBoard.getSelection(self.mainBoard.p2,output)  

                    self.removeCaptured()
                    self.updateAImoved(self.mainBoard.p2) 
                    self.legalMove(self.mainBoard.p2.getMoveSwapped())
                    

                    for i in range(len(self.spaceID)):
                        if(self.spaceID[i][0] == self.mainBoard.p2.getMoveSwapped()[0] and self.spaceID[i][1] == self.mainBoard.p2.getMoveSwapped()[1]):
                            self.checker = self.toChange
                            self.moveChecker(self.spaceID[i])
                            #print("red computer has moved from " + self.mainBoard.p2.getOriginalChecker() + " to " + self.mainBoard.p2.getMove())


                else:
                    print("red player has moved")


                if(self.mainBoard.win == False and self.mainBoard.turnTimer < 125):
                    self.mainBoard.turn(self.mainBoard.p2)
                    if(not self.mainBoard.p2.isRobot()):
                        self.playMainBoard()
                        self.removeCaptured()
                else:
                    self.mainBoard.p1.changeFitness(15)                                





    #setup so modular and can be used from either side of the board.
    #probably will have to steal from old code. Might need object check later on
    #to make sure clicked object is a space, not sure how to implement with new format.
    #can probably steal idea, not the code itself though. very messy, rewrite
    #!IMPORTANT!
    def legalMove(self,move): 
        checker=self.checker
        valid = False 

        if(self.human.isSelected):
            return

        if checker[4] == "Red":
            j=-1
            objA = "Red"
            jumpObj = self.blueObjects
        else:
            j=1
            objA = "Blue"
            jumpObj = self.redObjects

            
        #(Just runs again if its a king since it can move in either direction)
        for p in range(checker[0]):
            if p==1:
                j*=-1
            #checks if 'col' match each other            
            if move[1] == checker[2]+j:
                #checks if 'row' match each other
                if move[0] == checker[1]+1 or move[0] == checker[1]-1:
                    valid = True                        
                        
            for k in range(len(self.redObjects)):
                if move[0] == self.redObjects[k][1] and move[1] == self.redObjects[k][2]:
                    j = -10
            for k in range(len(self.blueObjects)):
                if move[0] == self.blueObjects[k][1] and move[1] == self.blueObjects[k][2]:
                    j = -10

            #checks if 'col' for jump match
            if move[1] == checker[2]+j*2:
                #checks to make sure 'row' for jump match
                if move[0] == checker[1]+2 or move[0] == checker[1]-2:

                    if (checker[4] == "Blue"):
                        for i in range(len(jumpObj)):
                            jmpChck = jumpObj[i]
                            if (jmpChck[2] == checker[2]+j and (jmpChck[1] == checker[1]+1 or jmpChck[1] == checker[1]-1)):     
                                try:
                                    self.canvas.delete(self.redObjects[i][3]) 
                                    self.redObjects.pop(i)
                                    
                                except:
                                    self.canvas.delete(self.blueObjects[i][3])
                                    self.blueObjects.pop(i)
                                valid = True 
                                break

                    else:
                        for i in range(len(self.blueObjects)):
                            jmpChck = self.blueObjects[i]
                            if (jmpChck[2] == checker[2]+j and (jmpChck[1] == checker[1]+1 or jmpChck[1] == checker[1]-1)):
                                self.canvas.delete(self.blueObjects[i][3])
                                self.blueObjects.pop(i)
                                valid = True
                                break
            if j == -10:
                valid = False

        if valid == True:
            self.human.setChoice(checker)
            if objA == "Red":
                self.redObjects[self.checkerI][1] = move[0]
                self.redObjects[self.checkerI][2] = move[1]
                if move[1] == 1 and self.checker[0] == 1:
                    #points = getStarPoints(getXY(checker[1],checker[2]),self.display_size)
                    #star = self.canvas.create_polygon(points,outline="gold",fill="gold",width=4)
                    self.redObjects[self.checkerI][0] = 2
                    #self.redObjects[self.checkerI][5] = star

            else:
                self.blueObjects[self.checkerI][1] = move[0]
                self.blueObjects[self.checkerI][2] = move[1]
                if move[1] == 8 and self.checker[0] == 1:
                    #points = getStarPoints(getXY(checker[1],checker[2]),self.display_size)
                    #star = self.canvas.create_polygon(points,outline="gold",fill="gold",width=4)
                    self.blueObjects[self.checkerI][0] = 2
                    #self.blueObjects[self.checkerI][5] = star

            self.human.setMove(move)
            self.human.isSelected = True
            return True
        return False



                
                
    def moveChecker(self,move):
        h =self.display_size
        x,y = getXY(move[0],move[1],h) 
        self.canvas.coords(self.checker[3],x,y,x+h/8,y+h/8)
        #self.canvas.coords(self.checker[5],getStarPoints(getXY(move[0],move[1],self.display_size)))
        self.checker = None




    #sets up the window 
    def boardWindow(self):
        root=Tk()
        root.wm_attributes("-topmost", 1)
        root.geometry(str(self.display_size)+'x'+str(self.display_size)  )
        root.title("Checkerboard")
        h=self.display_size
        self.canvas = Canvas(root, width=h,height=h)
        self.canvas.bind("<ButtonPress-1>",self.on_click)
        self.canvas.grid(row=0,column=0,columnspan=2)

        root.update_idletasks()
      
        #this is the program
        self.setup()
        root.mainloop()
        

