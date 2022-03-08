from tkinter import *
from board import *
import neat
import os
import time


##CONFIGURE THE STARTING BOARD SETTINGS
board_config = [
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]]
]

blue = [
[1,1,1],[1,1,3],[1,1,5],[1,1,7],
[1,2,2],[1,2,4],[1,2,6],[1,2,8],
[1,3,1],[1,3,3],[1,3,5],[1,3,7]]

red = [
[1,6,2],[1,6,4],[1,6,6],[1,6,8],
[1,7,1],[1,7,3],[1,7,5],[1,7,7],
[1,8,2],[1,8,4],[1,8,6],[1,8,8]]

gameType = None
fitnesses = []

#Gets the size of the screen being used.
def get_display_size():
    root = Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    height = root.winfo_screenheight()
    root.destroy()
    return height-250 #Arbitrary number to make height GUI smaller than screen


dp = get_display_size()

DispTXT=["Play as Blue!","Play as Red!","Play as Blue! (No GUI)","Play as Red! (No GUI)","Manually train NEAT","NEAT vs NEAT"]

button=[]
root=Tk()
root.title("What would you like to play as?")
root.geometry('350x200')
root.wm_attributes("-topmost", 1)


for i in range(6):
    b = Button(root, text=DispTXT[i], command= lambda i = i: multiFunky(i))
    b.pack()
    button.append(b)

def multiFunky(players):
    global gameType
    gameType = players
    for i in range(6):
        button[i].destroy()
    root.destroy()

    #strH=str(dp)+'x'+str(dp)  
    #root.geometry(strH)
    
root.mainloop()


##first paramater; True Human is red | False Human is Blue | None no Humans



def eval_genomes(genomes, config):
    global robots, geno, nets, currentGames
    robots = []
    geno = []
    nets = []
    currentGames = []
    i = 0

    for id, genome in genomes:
        ##creates the robots
        if i % 2 == 0:
            global robot
            robots.append(robot("Blue", [red,blue],i))
        else:
            robots.append(robot("Red" , [red,blue],i))
        i+=1

        geno.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

        
    for g, robot in enumerate(robots):
        geno[g].fitness = robot.getFitness()
    
                

    ##creates all the games 
    for r in range(len(robots)):  
        try:  
            currentGames.append(checkerboardClass(board_config, red, blue, robots[r],robots[r+1]))
        except:
            print("")
        r+=1
    
    #for each game, play through an entire game
    for g, game in enumerate(currentGames):
        while(game.win == False): ##while nobody has won, continue to run. 
            
            if (game.currentTurn == "Blue"):
                
                output = nets[g].activate(game.refreshData()) ##Red checkers, blue checkers. BLUE CHECKER ROBOT
                print(output[0])
                game.getSelection(game.p1,output[0])  
                
                print(game.p1.getOriginalChecker())
                print(game.p1.getFinalChecker())

                game.turn(game.p1)



            
            else:
                output = nets[g].activate(game.refreshData()) ##Red checkers, blue checkers. RED CHECKER ROBOT
                game.getSelection(game.p2,output[0])  

                print(game.p2.getOriginalChecker())
                print(game.p2.getFinalChecker())

                game.turn(game.p2)

                
            
            time.sleep(0.5)
            game.prettyBoard()
                  
        fitnesses.append(game.p1.getFitness())
        fitnesses.append(game.p2.getFitness())


        

def run_neat(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    pop.run(eval_genomes, 15) #number of runs

    
    # print("-----------------------------")
    # print("  Current generation: " + pop.generation+1)
    # best = -9999
    # for i in range(len(fitnesses)):
    #     if fitnesses[i] > best:
    #         best = fitnesses[i]
    # print("  Best Fitness Score: " + best)



if (__name__ == '__main__') and gameType == 5:
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat_config')
    run_neat(config_path)

