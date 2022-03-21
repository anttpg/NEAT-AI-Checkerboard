from math import e, sin
from tkinter import *
from board import *
import neat
import os
import random
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
runOnce = False

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
    global geno, nets, fitnesses, currentGames, redRobots, blueRobots, allRobots
    blueRobots = []
    redRobots = []
    allRobots = []
    geno = []
    nets = []
    currentGames = []
    fitnesses = []

    
    i = 0

    for id, genome in genomes:
        ##creates the robots
        if(runOnce == False):
            if i % 2 == 0:
                global robot
                r = robot("Blue", [red,blue],i)
                blueRobots.append(r)
            else:
                r =robot("Red" , [red,blue],i)
                redRobots.append(r)

            i+=1
            allRobots.append(r)

        geno.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    


    for g, robot in enumerate(allRobots):
        geno[g].fitness = robot.getFitness()
    
                

    ##creates all the games 
    if(runOnce == False):
        for r in range(len(allRobots)):  
            try:  
                currentGames.append(checkerboardClass(board_config, red, blue, blueRobots[r],redRobots[r]))
            except:
                print("")
            r+=1

    runOnce = True
    
    #for each game, play through an entire game
    for g, game in enumerate(currentGames):
        while(game.win == False): ##while nobody has won, continue to run. 
            if (game.currentTurn == "Blue"):
                
                output = nets[g].activate(game.refreshData()) 
                #print(output,(output[0] + output[1] + output[2] + output[3])/4, " Player 1")
                game.getSelection(game.p1,output)  
                
                #print(game.p1.getOriginalChecker())
                #print(game.p1.getFinalChecker())

                if(game.win == False and game.turnTimer < 125):
                    game.turn(game.p1)
                else:
                    game.p2.changeFitness(15)
                    break



            
            else:
                output = nets[g].activate(game.refreshData()) ##Red checkers, blue checkers. BLUE CHECKER ROBOT
                #print(output, " Player 2")
                game.getSelection(game.p2,output)  
                
                #print(game.p2.getOriginalChecker())
                #print(game.p2.getFinalChecker())

                if(game.win == False and game.turnTimer < 125):
                    game.turn(game.p2)
                else:
                    game.p1.changeFitness(15)
                    break
                
            
                
            
            #time.sleep(0.5)
        game.prettyBoard()
        game.p1.changeFitness((-0.1)*game.getTurn())
        game.p2.changeFitness((-0.1)*game.getTurn())
        fitnesses.append(game.p1.getFitness())
        fitnesses.append(game.p2.getFitness())
        

    random.shuffle(blueRobots)
    random.shuffle(redRobots)


def mod_sigmoid(x):
        if x == 0:
            return 0
        elif x == 1:
            return 1
        else:
            return (1/(1+((e)**(5-(10*x)))))
        

def run_neat(config_path):
    # Load configuration.
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    

    config.genome_config.add_activation('modified_sigmoid', mod_sigmoid)   



    # Create the population, which is the top-level object for a NEAT run.
    pop = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    # Run for up to 300 generations.
    winner = pop.run(eval_genomes, 15) #number of runs

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
    
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

