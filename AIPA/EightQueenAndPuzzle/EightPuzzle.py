import random
import math
import time
queens = [[0] * 8 for _ in range(8)]  # 8x8 chessboard
temp = [[0] * 8 for _ in range(8)]
totalTrial = 0  # Count of moves

# Randomly initialize the state
def initial():
    for i in range(8):
        for j in range(8):
            queens[i][j] = 0
    for i in range(8):
        num = random.randint(0, 7)
        queens[i][num] = 1

# Print the chessboard
def print_board(board):
    for row in board:
        print(' '.join(map(str, row)))

# Find the number of collisions at a given position
def find_collision(row, col):
    count = 0
    temp[row][col] = 1
    for k in range(64):
        if temp[k // 8][k % 8] == 1:
            for i in range(8):
                if i != k // 8 and temp[i][k % 8] == 1:
                    count += 1
            for i, j in zip(range(k // 8, 8), range(k % 8, 8)):  # Right-down
                if i != k // 8 and temp[i][j] == 1:
                    count += 1
            for i, j in zip(range(k // 8, -1, -1), range(k % 8, -1, -1)):  # Left-up
                if i != k // 8 and temp[i][j] == 1:
                    count += 1
            for i, j in zip(range(k // 8, 8), range(k % 8, -1, -1)):  # Left-down
                if i != k // 8 and temp[i][j] == 1:
                    count += 1
            for i, j in zip(range(k // 8, -1, -1), range(k % 8, 8)):  # Right-up
                if i != k // 8 and temp[i][j] == 1:
                    count += 1
    temp[row][col] = 0
    return count // 2

# Check if there are no collisions in the board
def check(board):
    for i in range(8):
        flag = False
        for j in range(8):
            if board[i][j] == 1 and find_collision(i, j) == 0:
                flag = True
                break
        if not flag:
            return False
    return True

# Hill Climbing algorithm
def hill_climbing():
    for trial in range(101):
        # Copy the original board data to temp
        for i in range(8):
            for j in range(8):
                temp[i][j] = queens[i][j]
        h = [[0] * 8 for _ in range(8)]
        min_h = 9999
        min_x = 0
        min_y = 0
        cur_state = 0
        for i in range(8):
            for j in range(8):
                for k in range(8):
                    temp[i][k] = 0
                h[i][j] = find_collision(i, j)
                if queens[i][j] == 1:
                    cur_state = h[i][j]
                if h[i][j] < min_h:
                    min_h = h[i][j]
                    min_x = i
                    min_y = j
                for k in range(8):
                    temp[i][k] = queens[i][k]

        if cur_state > min_h:
            for i in range(8):
                queens[min_x][i] = 0
            queens[min_x][min_y] = 1

        if check(h):
            global totalTrial
            totalTrial += trial
            return True
    return False

# First-choice Hill Climbing algorithm
def first_choice():
    for trial in range(101):
        for i in range(8):
            for j in range(8):
                temp[i][j] = queens[i][j]
        h = [[0] * 8 for _ in range(8)]
        cur_state = 0
        for i in range(8):
            for j in range(8):
                for k in range(8):
                    temp[i][k] = 0
                h[i][j] = find_collision(i, j)
                if queens[i][j] == 1:
                    cur_state = h[i][j]
                for k in range(8):
                    temp[i][k] = queens[i][k]
        better = False
        times = 0
        next = 0
        next_state = 0
        while not better:
            next = random.randint(0, 63)
            next_state = h[next // 8][next % 8]
            if next_state < cur_state:
                better = True
            times += 1
            if times > 100:
                break
        if better:
            for i in range(8):
                queens[next // 8][i] = 0
            queens[next // 8][next % 8] = 1
        if check(h):
            global totalTrial
            totalTrial += trial
            return True
    return False

# Simulated Annealing algorithm
def simulated_annealing():
    temperature = 5
    trial = 0
    while temperature > 0.00001:
        for i in range(8):
            for j in range(8):
                temp[i][j] = queens[i][j]
        h = [[0] * 8 for _ in range(8)]
        cur_state = 0
        for i in range(8):
            for j in range(8):
                for k in range(8):
                    temp[i][k] = 0
                h[i][j] = find_collision(i, j)
                if queens[i][j] == 1:
                    cur_state = h[i][j]
                for k in range(8):
                    temp[i][k] = queens[i][k]
        better = False
        times = 0
        next = random.randint(0, 63)
        next_state = h[next // 8][next % 8]
        E = next_state - cur_state
        if E < 0:
            better = True
        elif math.exp((-1) * E / temperature) > (random.randint(0, 999) / 1000):
            better = True
        if better:
            for i in range(8):
                queens[next // 8][i] = 0
            queens[next // 8][next % 8] = 1
            trial += 1
        if check(h):
            global totalTrial
            totalTrial += trial
            return True
        temperature *= 0.99
    return False

# Steepest Ascent Hill Climbing
def steepest_ascent():
    count = 0
    for i in range(1000):
        initial()
        if hill_climbing():
            count += 1
    return count

# First-choice Hill Climbing
def first_choice_search():
    count = 0
    for i in range(1000):
        initial()
        if first_choice():
            count += 1
    return count

# Random Restart Hill Climbing
def random_restart():
    find = False
    while not find:
        initial()
        find = hill_climbing()
    return find

# Simulated Annealing Search
def simulated_annealing_search():
    count = 0
    for i in range(1000):
        initial()
        if simulated_annealing():
            count += 1
    return count

if __name__ == '__main__':
    random.seed(time.time())

    totalTrial = 0
    print("Steepest-Ascent searching...")
    count = steepest_ascent()
    print("Steepest-Ascent [success/total]:", count, "/1000")
    # print("Average steps:", totalTrial / count)

    # totalTrial = 0
    # print("Random-Restart searching...")
    # count2 = random_restart()
    # print("Random-Restart:", count2)
    # print("Average steps:", totalTrial / count2)

    totalTrial = 0
    print("First-Choice searching...")
    count3 = first_choice_search()
    print("First-Choice [success/total]:", count3, "/1000")
    # print("Average steps:", totalTrial / count3)

    totalTrial = 0
    print("Simulated-Annealing searching...")
    count4 = simulated_annealing_search()
    print("Simulated-Annealing [success/total]:", count4, "/1000")
    # print("Average steps:", totalTrial / count4)
