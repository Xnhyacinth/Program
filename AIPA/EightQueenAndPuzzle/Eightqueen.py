import random
import math
import time

# heuristic cost
def getCollisionNum(board):
    num = 0
    for col in range(len(board)):
        for anotherCol in range(col+1, len(board)):
            if board[col] == board[anotherCol]:
                num += 1 # collied in the same row
            elif abs(board[col] - board[anotherCol]) == (anotherCol - col):
                num += 1 # collied diagonally
    return num

# heuristic cost
def getCollisionNum(board):
    num = 0
    for col in range(len(board)):
        for anotherCol in range(col+1, len(board)):
            if board[col] == board[anotherCol]:
                num += 1 # collied in the same row
            elif abs(board[col] - board[anotherCol]) == (anotherCol - col):
                num += 1 # collied diagonally
    return num

def main():
    f = open("eightQueensTest.txt", "w")
    testCaseCount = 1000
    board = ""
    while testCaseCount > 0:
        testCaseCount -= 1
        for col in range(0,7):
            board += str(random.randint(0,7)) + ' '
        board += str(random.randint(0,7)) + '\n'
    f.write(board)
    f.close()

# for each column, calculate the collision number
# if the queen is moved to the other rows
# find the smallest one and move to it.
def step_steepestHillClimbing(board):
    collisionNumBoard = {}
    smallestCollisionNum = getCollisionNum(board)
    for col in range(len(board)):
        for row in range(len(board)):
            if board[col] == row:
                continue
            originRow = board[col]
            board[col] = row
            collisionNumBoard[(row,col)] = getCollisionNum(board)
            board[col] = originRow
    
    
    for point,value in collisionNumBoard.items():
        if value < smallestCollisionNum:
            smallestCollisionNum = value
    
    smallestCollisionPoints = []
    for point,value in collisionNumBoard.items():
        if value == smallestCollisionNum:
            smallestCollisionPoints.append(point)
    
    # can not find a steeper move
    # we have come to the peek(local optimization)
    if len(smallestCollisionPoints) == 0:
        #print "local optimization"
        global FAILED
        FAILED = True
        return board
    
    random.shuffle(smallestCollisionPoints)
    board[smallestCollisionPoints[0][1]]=smallestCollisionPoints[0][0]
    return board

# randomly select a point until it is 
# better than the original one
# change "better than" to "not worse than"
# can significantly increase the success rate
def step_FirstChoiceHillClimbing(board):
    collisionNum = getCollisionNum(board)
    maxRound = 1000
    count = 0
    while True:
        count += 1
        if(count >= maxRound):
            global FAILED
            FAILED = True
            return board
        randomRow = random.randint(0,len(board)-1)
        randomCol = random.randint(0,len(board)-1)
        if board[randomCol] == randomRow:
            continue
        originRow = board[randomCol]
        board[randomCol] = randomRow
        if getCollisionNum(board) <= collisionNum: # not worse than
            return board
        board[randomCol] = originRow

def step_RandomHillClimbing(board):
    while True:
        randomRow = random.randint(0,len(board)-1)
        randomCol = random.randint(0,len(board)-1)
        if board[randomCol] != randomRow:
            board[randomCol] = randomRow
            return board
    
    return board

# accept the random choice with certain probability
def step_SimulatedAnnealing(board):
    temperature = len(board)**2
    annealingRate = 0.95
    while True:
        randomRow = random.randint(0,len(board)-1)
        randomCol = random.randint(0,len(board)-1)
        originCollisionNum = getCollisionNum(board)
        originRow = board[randomCol]
        board[randomCol] = randomRow
        newCollisionNum = getCollisionNum(board)
        temperature = max(temperature * annealingRate, 0.02)
        if newCollisionNum < originCollisionNum:
            return board
        else:
            deltaE = newCollisionNum - originCollisionNum
            acceptProbability = min(math.exp(deltaE / temperature), 1)
            if random.random() <= acceptProbability:
                return board
            else:
                board[randomCol] = originRow
    
    return board

def solution_FirstChoiceHillClimbing(board):
    maxRound = 1000 # the expected number to find a solution
    count = 0
    while True:
        collisionNum = getCollisionNum(board)
        if collisionNum == 0:
            return board
        board = step_FirstChoiceHillClimbing(board)
        global FAILED
        if FAILED:
            return board
        count += 1
        if(count >= maxRound):
            FAILED = True
            return board

def solution_SimulatedAnnealing(board):
    maxRound = 500000 # the expected number to find a solution
    count = 0
    while True:
        collisionNum = getCollisionNum(board)
        if collisionNum == 0:
            return board
        board = step_SimulatedAnnealing(board)
        global FAILED
        if FAILED:
            return board
        count += 1
        if(count >= maxRound):
            FAILED = True
            return board

def solution_RandomHillClimbing(board):
    maxRound = 500000 # the expected number to find a solution
    count = 0
    while True:
        collisionNum = getCollisionNum(board)
        if collisionNum == 0:
            return board
        board = step_RandomHillClimbing(board)
        global FAILED
        if FAILED:
            return board
        count += 1
        if(count >= maxRound):
            FAILED = True
            return board

def solution_steepestHillClimbing(board):
    maxRound = 200 # the expected number to find a solution
    count = 0
    while True:
        collisionNum = getCollisionNum(board)
        if collisionNum == 0:
            return board
        board = step_steepestHillClimbing(board)
        global FAILED
        if FAILED:
            return board
        count += 1
        if(count >= maxRound):
            FAILED = True
            return board

if __name__ == '__main__':
    # main()
    successCase = [0, 0, 0, 0]
    ts = []
    result = None
    global FAILED
    with open("eightQueensTest.txt", "r") as ins:
        x0 = time.time()
        for line in ins:
            FAILED = False
            board = []
            for col in line.split():
                board.append(int(col))        
            # FAILED = False
            board = solution_steepestHillClimbing(board) # 换成对应的方法
            print(board)
            if FAILED:
                result = "Failed!"
            else:
                successCase[0] += 1
        ts.append(time.time() - x0)
    with open("eightQueensTest.txt", "r") as ins:
        x0 = time.time()
        for line in ins:
            FAILED = False
            board = []
            for col in line.split():
                board.append(int(col))
            board = solution_FirstChoiceHillClimbing(board) # 换成对应的方法
            if FAILED:
                result = "Failed!"
            else:
                successCase[1] += 1
                for col in range(len(board)):
                    result == str(board[col]) + " "
        ts.append(time.time() - x0)
            # FAILED = False
    # with open("eightQueensTest.txt", "r") as ins:
    #     x0 = time.time()
    #     for line in ins:
    #         FAILED = False
    #         board = []
    #         for col in line.split():
    #             board.append(int(col))        
    #         board = solution_RandomHillClimbing(board) # 换成对应的方法
    #         if FAILED:
    #             result = "Failed!"
    #         else:
    #             successCase[2] += 1
    #         # FAILED = False
    #     ts.append(time.time() - x0)
    # with open("eightQueensTest.txt", "r") as ins:
    #     x0 = time.time()
    #     for line in ins:
    #         FAILED = False
    #         board = []
    #         for col in line.split():
    #             board.append(int(col))        
    #         board = solution_SimulatedAnnealing(board) # 换成对应的方法
    #         if FAILED:
    #             result = "Failed!"
    #         else:
    #             successCase[3] += 1
    #     ts.append(time.time() - x0)
            # result += "\n"
    print(ts)
    print(successCase)