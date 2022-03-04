import tst
c = []

c = tst.chasa(23)
print(c.blu)



legalJumps = [[1,1],[2,2],[1,-1],[2,-2],[-1,-1],[-2,-2],[-1,1],[-2,2]]
for i in range(8):
    if(i % 2 == 0):
        print(legalJumps[i])


blueCheckers = [
[1,1,1],[1,1,3],[1,1,5],[1,1,7],
[1,2,2],[1,2,4],[1,2,6],[1,2,8],
[2,3,1],[2,3,3],[1,3,5],[1,3,7]]

redCheckers = [
[1,6,2],[1,6,4],[1,6,6],[1,6,8],
[1,7,1],[1,7,3],[1,7,5],[1,7,7],
[1,8,2],[1,8,4],[1,8,6],[1,8,8]]

board = [
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]]
]

print(1%2 == 3%2)

def legalChoice(choice,color):
    if color == "Blue":
        if(choice in blueCheckers):
            return True
        
    else:
        if(choice in redCheckers): 
            return True
    
    return False


for y in range(7):
    for x in range(7):
        if y % 2 == x % 2:
            if legalChoice([1,y+1,x+1],"Blue"):
                board[y][x] = "b"
            elif legalChoice([2,y+1,x+1],"Blue"):
                board[y][x] = "B" 
            elif legalChoice([1,y+1,x+1],"Red"):
                board[y][x] = "r"
            elif legalChoice([2,y+1,x+1],"Red"):
                board[y][x] = "R"
            else:
                board[y][x] = "_"

        else:                   
            board[y][x] = "#"

    print(board[y][0],board[y][1],board[y][2],board[y][3],board[y][4],board[y][5],board[y][6],board[y][7])
    
        


