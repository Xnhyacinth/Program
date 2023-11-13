import random
import time
import math
# heuristic cost
# manhattan_distance
def getManhattanDistance(board):
    distance = 0
    for i in range(len(board)):
        distance += abs(i/3 - board[i]/3) + abs(i%3 - board[i]%3)
    return distance

# for each column, calculate the collision number
# if the queen is moved to the other rows
# find the smallest one and move to it.
def step_steepestHillClimbing(board):
    for i in range(len(board)):
        if board[i] == 0:
            break
    distanceBoard = {}
    if i >= 3:
        upBoard = list(board)
        upBoard[i] = board[i-3]
        upBoard[i-3] = 0
        distanceBoard[i-3] = getManhattanDistance(upBoard)
    if i < 6:
        downBoard = list(board)
        downBoard[i] = board[i+3]
        downBoard[i+3] = 0
        distanceBoard[i+3] = getManhattanDistance(downBoard)
    if i%3 != 0:
        leftBoard = list(board)
        leftBoard[i] = board[i-1]
        leftBoard[i-1] = 0
        distanceBoard[i-1] = getManhattanDistance(leftBoard)
    if (i+1)%3 != 0:
        rightBoard = list(board)
        rightBoard[i] = board[i+1]
        rightBoard[i+1] = 0
        distanceBoard[i+1] = getManhattanDistance(rightBoard)
    
    shortestDistance = getManhattanDistance(board)
    for point,value in distanceBoard.items():
        # "<=" means "not worse than" situation
        # plain
        if value <= shortestDistance:
            shortestDistance = value
    
    shortestDistancePoints = []
    for point,value in distanceBoard.items():
        if value == shortestDistance:
            shortestDistancePoints.append(point)
    
    # can not find a steeper move
    # we have come to the peek(local optimization)
    if len(shortestDistancePoints) == 0:
        # print "local optimization"
        global FAILED
        FAILED = True
        return board
    
    random.shuffle(shortestDistancePoints)
    board[i] = board[shortestDistancePoints[0]]
    board[shortestDistancePoints[0]]= 0
    return board

def solution_steepestHillClimbing(board):
    # For each case, there are only several situations using this solution.
    # In average, we will reach a local optimization within 100 steps
    # or fall into a infinite loop (a plain) within 100 steps.
    maxRound = 50000
    count = 0
    while True:
        count += 1
        collisionNum = getManhattanDistance(board)
        # print count, collisionNum
        if collisionNum == 0:
            return board
        board = step_steepestHillClimbing(board)
        global FAILED
        if FAILED:
            return board
        if(count >= maxRound):
            # for i in range(0,len(board)):
            #     print board[i]
            FAILED = True
            return board
        
def step_FirstChoiceHillClimbing(board):
    for i in range(len(board)):
        if board[i] == 0:
            break
    distance = getManhattanDistance(board)
    maxRound = 500 # the expected rounds to produce all the 4 directions
    count = 0
    while True:
        count += 1
        if(count >= maxRound):
            global FAILED
            FAILED = True
            return board
        randCase = random.randint(0,4)
        if randCase == 0:
            if i >= 3:
                upBoard = list(board)
                upBoard[i] = board[i-3]
                upBoard[i-3] = 0
                if getManhattanDistance(upBoard) < distance:
                    return upBoard
        elif randCase == 1:
            if i < 6:
                downBoard = list(board)
                downBoard[i] = board[i+3]
                downBoard[i+3] = 0
                if getManhattanDistance(downBoard) < distance:
                    return downBoard
        elif randCase == 2:
            if i%3 != 0:
                leftBoard = list(board)
                leftBoard[i] = board[i-1]
                leftBoard[i-1] = 0
                if getManhattanDistance(leftBoard) < distance:
                    return leftBoard
        else:    
            if (i+1)%3 != 0:
                rightBoard = list(board)
                rightBoard[i] = board[i+1]
                rightBoard[i+1] = 0
                if getManhattanDistance(rightBoard) < distance:
                    return rightBoard
        
    return board

def solution_FirstChoiceHillClimbing(board):
    maxRound = 20000
    count = 0
    while True:
        collisionNum = getManhattanDistance(board)
        if collisionNum == 0:
            return board
        board = step_FirstChoiceHillClimbing(board)
        count += 1
        if(count >= maxRound):
            global FAILED
            FAILED = True
            return board

def step_RandomHillClimbing(board):
    for i in range(len(board)):
        if board[i] == 0:
            break
    while True:
        randCase = random.randint(0,4)
        if randCase == 0:
            if i >= 3:
                upBoard = list(board)
                upBoard[i] = board[i-3]
                upBoard[i-3] = 0
                return upBoard
        elif randCase == 1:
            if i < 6:
                downBoard = list(board)
                downBoard[i] = board[i+3]
                downBoard[i+3] = 0
                return downBoard
        elif randCase == 2:
            if i%3 != 0:
                leftBoard = list(board)
                leftBoard[i] = board[i-1]
                leftBoard[i-1] = 0
                return leftBoard
        else:    
            if (i+1)%3 != 0:
                rightBoard = list(board)
                rightBoard[i] = board[i+1]
                rightBoard[i+1] = 0
                return rightBoard
        
    return board

def solution_RandomHillClimbing(board):
    maxRound = 500000
    count = 0
    while True:
        distance = getManhattanDistance(board)
        if distance == 0:
            return board
        board = step_RandomHillClimbing(board)
        count += 1
        if(count >= maxRound):
            global FAILED
            FAILED = True
            return board
        
# accept the random choice with certain probability
def step_SimulatedAnnealing(board):
    temperature = len(board)
    annealingRate = 0.95
    
    for i in range(len(board)):
        if board[i] == 0:
            break
    distance = getManhattanDistance(board)
    temperature = max(temperature * annealingRate, 0.02)
    while True:
        randCase = random.randint(0,4)
        if randCase == 0:
            if i >= 3:
                upBoard = list(board)
                upBoard[i] = board[i-3]
                upBoard[i-3] = 0
                if getManhattanDistance(upBoard) < distance:
                    return upBoard
                else:
                    deltaE = getManhattanDistance(upBoard) - distance
                    acceptProbability = min(math.exp(deltaE / temperature), 1)
                    if random.random() <= acceptProbability:
                        return upBoard
        elif randCase == 1:
            if i < 6:
                downBoard = list(board)
                downBoard[i] = board[i+3]
                downBoard[i+3] = 0
                if getManhattanDistance(downBoard) < distance:
                    return downBoard
                else:
                    deltaE = getManhattanDistance(downBoard) - distance
                    acceptProbability = min(math.exp(deltaE / temperature), 1)
                    if random.random() <= acceptProbability:
                        return downBoard
        elif randCase == 2:
            if i%3 != 0:
                leftBoard = list(board)
                leftBoard[i] = board[i-1]
                leftBoard[i-1] = 0
                if getManhattanDistance(leftBoard) < distance:
                    return leftBoard
                else:
                    deltaE = getManhattanDistance(leftBoard) - distance
                    acceptProbability = min(math.exp(deltaE / temperature), 1)
                    if random.random() <= acceptProbability:
                        return leftBoard
        else:    
            if (i+1)%3 != 0:
                rightBoard = list(board)
                rightBoard[i] = board[i+1]
                rightBoard[i+1] = 0
                if getManhattanDistance(rightBoard) < distance:
                    return rightBoard
                else:
                    deltaE = getManhattanDistance(rightBoard) - distance
                    acceptProbability = min(math.exp(deltaE / temperature), 1)
                    if random.random() <= acceptProbability:
                        return rightBoard
                    
    return board

def solution_SimulatedAnnealing(board):
    # the success rate will increase by increasing the maxRound
    maxRound = 500000
    count = 0
    while True:
        collisionNum = getManhattanDistance(board)
        if collisionNum == 0:
            return board
        board = step_SimulatedAnnealing(board)
        count += 1
        if(count >= maxRound):
            global FAILED
            FAILED = True
            return board        

def solution_generate(board):
    maxStep = 5000
    count = 0
    while True:
        board = step_RandomHillClimbing(board)
        count += 1
        if(count >= maxStep):
            return board

def generate():
    f = open("eightPuzzleTest.txt", "w")
    testCaseCount = 1000
    result = ""
    while testCaseCount > 0:
        board = [0,1,2,3,4,5,6,7,8]
        testCaseCount -= 1
        
        board = solution_generate(board)
        
        for i in range(0,8): # i = 0 1 2 3 4 5 6 7
            result += str(board[i]) + ' '
        result += str(board[i+1]) + '\n' #! i+1=8
    f.write(result)
    f.close()

def main():
    generate()
    title = "EightPuzzle_FirstChoiceHillClimbing"
    startTime = time.time()
    successCase = 0
    totalCase = 0
    result = title + " result:\n\n"
    with open("eightPuzzleTest.txt", "r") as ins:
        for line in ins:
            global FAILED
            FAILED = False
            totalCase += 1
            board = []
            for col in line.split():
                board.append(int(col))
            board = solution_FirstChoiceHillClimbing(board)
            if FAILED:
                result += "Failed!"
            else:
                successCase += 1
                for col in range(len(board)):
                    result += str(board[col]) + " "
            result += "\n"
    
    endTime = time.time()
    result += "\nTotal time: " + str(endTime - startTime) + '\n'
    result += "Total case number: " + str(totalCase) + ", Success case number: " + str(successCase) + '\n'
    result += "Success rate: " + str(successCase / float(totalCase)) + '\n'
    
    f = open(title + '.txt', 'w')
    f.write(result)
    f.close()

    title = "EightPuzzle_steepestHillClimbing"
    startTime = time.time()
    successCase = 0
    totalCase = 0
    result = title + " result:\n\n"
    with open("eightPuzzleTest.txt", "r") as ins:
        for line in ins:
            FAILED = False
            totalCase += 1
            board = []
            for col in line.split():
                board.append(int(col))
            board = solution_steepestHillClimbing(board)
            if FAILED:
                result += "Failed!"
            else:
                successCase += 1
                for col in range(len(board)):
                    result += str(board[col]) + " "
            result += "\n"
    
    endTime = time.time()
    result += "\nTotal time: " + str(endTime - startTime) + '\n'
    result += "Total case number: " + str(totalCase) + ", Success case number: " + str(successCase) + '\n'
    result += "Success rate: " + str(successCase / float(totalCase)) + '\n'
    # print result
    
    f = open(title + '.txt', 'w')
    f.write(result)
    f.close()

    # title = "EightPuzzle_SimulatedAnnealing"
    # startTime = time.time()
    # successCase = 0
    # totalCase = 0
    # result = title + " result:\n\n"
    # with open("eightPuzzleTest.txt", "r") as ins:
    #     for line in ins:
    #         FAILED = False
    #         totalCase += 1
    #         board = []
    #         for col in line.split():
    #             board.append(int(col))
    #         board = solution_SimulatedAnnealing(board)
    #         if FAILED:
    #             result += "Failed!"
    #         else:
    #             successCase += 1
    #             for col in range(len(board)):
    #                 result += str(board[col]) + " "
    #         result += "\n"
    
    # endTime = time.time()
    # result += "\nTotal time: " + str(endTime - startTime) + '\n'
    # result += "Total case number: " + str(totalCase) + ", Success case number: " + str(successCase) + '\n'
    # result += "Success rate: " + str(successCase / float(totalCase)) + '\n'
    
    # f = open(title + '.txt', 'w')
    # f.write(result)
    # f.close()
    
    # title = "EightPuzzle_RandomHillClimbing"
    # startTime = time.time()
    # successCase = 0
    # totalCase = 0
    # result = title + " result:\n\n"
    # with open("eightPuzzleTest.txt", "r") as ins:
    #     for line in ins:
    #         FAILED = False
    #         totalCase += 1
    #         board = []
    #         for col in line.split():
    #             board.append(int(col))
    #         board = solution_RandomHillClimbing(board)
    #         if FAILED:
    #             result += "Failed!"
    #         else:
    #             successCase += 1
    #             for col in range(len(board)):
    #                 result += str(board[col]) + " "
    #         result += "\n"
    
    # endTime = time.time()
    # result += "\nTotal time: " + str(endTime - startTime) + '\n'
    # result += "Total case number: " + str(totalCase) + ", Success case number: " + str(successCase) + '\n'
    # result += "Success rate: " + str(successCase / float(totalCase)) + '\n'
    
    # f = open(title + '.txt', 'w')
    # f.write(result)
    # f.close()

if __name__ == '__main__':
    main()
