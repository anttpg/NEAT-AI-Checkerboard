from tkinter import *




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



class checkerboardClass:

    initial = []
    spaceID = []
    redObjects = []
    blueObjects = []
    turn = "blue"
    canvas = None
    checker = None
    deleteChecker = None
    display_size = None
    checkerI = 0
    
    robot1 = None
    robot2 = None
    

    def __init__(self, players,display,init):
        if players == 0: 
            self.turn = "red"
            self.robot1 = robot("blue")
        if players == 1:
            self.turn = "blue"
            self.robot1 = robot("red")
        if players == 2:
            self.robot1 = robot("blue")
            self.robot2 = robot("red")
        if players == 3:
            self.turn = "red"
            
        self.display_size = display
        self.initial = init
        

    #Grapics; self explanitory
    def ring(self,w):    
        if self.checker != None:
            self.canvas.itemconfig(self.checker[3], outline='gold',width = w)   


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

        self.blueObjects = self.draw_checkers(self.initial[0],"blue")
        self.redObjects = self.draw_checkers(self.initial[1],"red")
        del self.initial
               

    def on_click(self, event):
        turn = self.turn
        self.ring(0)
        #Find clicked object
        clickedObject = self.canvas.find_closest(event.x, event.y)[0]
        self.play(clickedObject)


    def run(self):
        robot1 = self.robot1
        robot2 = self.robot2
        try:
            print('catch 1a')
            if robot1.isComputerMove(self.turn):
                print('catch 2a')
                robot1.randomizeMove()
                self.checker=robot1.getChecker()
                print(robot1.getChecker())
                while self.legalMove(robot1.getMove()) == False: 
                    robot1.randomizeMove()

                self.moveChecker(robot1.getMove())
        except:
            pass
        try:
            
            if robot2.isComputerMove(self.turn):
                print('catch 4a')
                robot2.randomizeMove()
                self.checker=robot2.getChecker()
                print(robot2.getChecker())
                while self.legalMove(robot2.getMove()) == False: 
                    robot2.randomizeMove()
                
                self.moveChecker(robot2.getMove())
            print('catch 3a PASS')
        except:
            pass
        
     






    
    def play(self,clickedObject):
        clickID = clickedObject
        for i in range(len(self.spaceID)):
            #if clicked object is a space
            if self.spaceID[i][2] == clickID and self.checker != None:
                if self.legalMove(self.spaceID[i]):
                    self.moveChecker(self.spaceID[i])
                    
                    


        for i in range(len(self.blueObjects)):
            if self.blueObjects[i][3] == clickID and self.turn == "blue":
                self.checker = self.blueObjects[i]
                self.checkerI = i
                self.ring(10)        

        for i in range(len(self.redObjects)):
            if self.redObjects[i][3] == clickID and self.turn == "red":
                self.checker = self.redObjects[i]
                self.checkerI = i
                self.ring(10)
        



    #setup so modular and can be used from either side of the board.
    #probably will have to steal from old code. Might need object check later on
    #to make sure clicked object is a space, not sure how to implement with new format.
    #can probably steal idea, not the code itself though. very messy, rewrite
    #!IMPORTANT!
    def legalMove(self,move): 
        checker=self.checker
        valid = False 
        if checker[4] == "red":
            j=-1
            objA = "red"
            jumpObj = self.blueObjects
        else:
            j=1
            objA = "blue"
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

                    if (checker[4] == "blue"):
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
            if objA == "red":
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

            return True
        return False



                
                
    def moveChecker(self,move):
        h =self.display_size
        x,y = getXY(move[0],move[1],h) 
        self.canvas.coords(self.checker[3],x,y,x+h/8,y+h/8)
        #self.canvas.coords(self.checker[5],getStarPoints(getXY(move[0],move[1],self.display_size)))
        if self.turn == "red":
            self.turn = "blue"
        else:
            self.turn = "red"
        self.checker = None



        



    #sets up the window 
    def boardWindow(self, root):
        root.title("Checkerboard")
        h=self.display_size
        self.canvas = Canvas(root, width=h,height=h)
        self.canvas.bind("<ButtonPress-1>",self.on_click)
        self.canvas.grid(row=0,column=0,columnspan=2)

        root.update_idletasks()
      
        #this is the program
        self.setup()
        self.run()
        root.mainloop()

