from board import Board
import os
import n_net
import time
import datetime
from multiprocessing import Pool

def genInitialData():
    with open('statistics.csv', 'w+') as file:
        file.close()
    data = list(map(lambda x: n_net.neuralNetwork(100,200,3,0.3), [None]*100))
    print("Generated initial data.")
    
    return data

def mateSnakes(left, right):
    return left.mate(right)

def brainToBoard(brain):
    return Board(10,10, train=False, brain=brain)

def createPopulation(seed):
    timestamp = time.time()
    print()
    print('Creating population from seed.')
    pool = Pool()
    boards = pool.map(brainToBoard, seed)
    tmp = []
    for i in range(10):                 # 20 initial subjects, 10 pairs generating 8 children each
        for _ in range(8):
            #boards.append(Board(10, 10, train = False, brain = boards[i*2].snake.brain.mate(boards[i*2+1].snake.brain)))
            tmp.append(pool.apply_async(mateSnakes, args=( seed[i*2], seed[i*2+1] ) ) )
    pool.close()
    pool.join()
    for i in tmp:
        boards.append(Board(10, 10, train = False, brain = i.get()))
    print('Population created in', time.strftime("%H:%M:%S", time.gmtime(int((time.time() - timestamp)))))
    print()
    return boards

def loadData():
    try:
        print('Attemtpting to load previous session data.')
        brains = [None] * 20
        for i in range(20):
            brains[i] = n_net.neuralNetwork.load('.\\latest_data\\'+str(i))
        with open('.\\latest_data\\gen','r') as file:
            generation = int(file.readline().strip())
            file.close()
            print('Session data loaded.')
            return (brains, generation)
    except:
        print('Error loading data, generating new session.')
        return (genInitialData(),1)

def saveSession(boards, generation):
    print("Saving session data.")
    timestampstr = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d---%H_%M_%S')+'_gen' + str(generation)
    try:
        os.makedirs(timestampstr)
    except FileExistsError:
        None
    try:
        os.makedirs('latest_data')
    except FileExistsError:
        None
    for i in range(20):
        boards[i].snake.brain.save('.\\'+timestampstr+'\\' + str(i))
        boards[i].snake.brain.save('.\\latest_data\\' + str(i))
    with open('.\\'+timestampstr+'\\' + 'gen','w') as file:
        print(str(generation), file=file)
        file.close()
    with open('.\\latest_data\\' + 'gen','w') as file:
        print(str(generation), file=file)
        file.close()
    print('Session data save complete.')

def processBoard(board, tests = 250):
    scoreTotal = 0
    for _ in range(tests):
        board.resetBoard()
        while board.frame(display = False):
            None
        scoreTotal = scoreTotal + board.score
    return scoreTotal / tests

def main():
    (initialPop, generation) = loadData()
    boards = createPopulation(initialPop)
    saveInterval = 100
    saveCooldown = saveInterval - 1
    while True:
        print("Evaluating generation #" + str(generation))
        startTimestamp = time.time()
        pool = Pool()
        results = pool.map(processBoard, boards)
        pool.close()
        pool.join()
        #results = list(map(lambda x: processBoard(x), boards))
        results.sort(reverse=True)
        print('Calculation time:',time.strftime("%H:%M:%S", time.gmtime(int(time.time() - startTimestamp))))
        print("Average score", sum(results)/len(results))
        print("Top 20 subjects:")
        for i in range(5):
            for j in range(4):
                print(str(i)+":", results[i*4+j], end = '')      
            print()
        print()
        boards.sort(key = lambda x: x.score, reverse = True)
        for i in range(20):
            initialPop[i] = boards[i].snake.brain
        boards = createPopulation(initialPop)
        if saveCooldown == 0:
            saveSession(boards, generation+1)
            saveCooldown = saveInterval - 1
            with open('statistics.csv', 'a+') as stats:
                print(str(generation)+';' + str(int((sum(results)/len(results))*1000)/1000.0), file = stats)
        else:
            saveCooldown = saveCooldown - 1
        generation = generation + 1
if __name__ == '__main__':
    main()