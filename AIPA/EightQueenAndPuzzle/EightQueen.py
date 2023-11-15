import random
import math
import time

queens = [[0] * 8 for _ in range(8)]  # 8x8 chessboard
temp = [[0] * 8 for _ in range(8)]
total_trial = 0  # count the number of moves


# Randomly generate initial state
def initial():
    for i in range(8):
        for j in range(8):
            queens[i][j] = 0
    for i in range(8):
        num = random.randint(0, 7)
        queens[i][num] = 1


def print_board():
    for i in range(8):
        for j in range(8):
            print(queens[i][j], end=" ")
        print()


# Count the number of conflicts for all queens at a given position
def find_collision(row, col):
    count = 0
    temp[row][col] = 1

    for k in range(64):
        if temp[k // 8][k % 8] == 1:
            for i in range(8):  # Same column
                if i != k // 8 and temp[i][k % 8] == 1:
                    count += 1
            for i, j in zip(range(k // 8, 8), range(k % 8, 8)):  # Right-down diagonal
                if i != k // 8 and temp[i][j] == 1:
                    count += 1
            for i, j in zip(range(k // 8, -1, -1), range(k % 8, -1, -1)):  # Left-up diagonal
                if i != k // 8 and temp[i][j] == 1:
                    count += 1
            for i, j in zip(range(k // 8, 8), range(k % 8, -1, -1)):  # Left-down diagonal
                if i != k // 8 and temp[i][j] == 1:
                    count += 1
            for i, j in zip(range(k // 8, -1, -1), range(k % 8, 8)):  # Right-up diagonal
                if i != k // 8 and temp[i][j] == 1:
                    count += 1

    temp[row][col] = 0  # Restore position
    return count // 2


def check(h):
    for i in range(8):
        flag = False
        for j in range(8):
            if queens[i][j] == 1 and h[i][j] == 0:
                flag = True
                break
        if not flag:
            return False
    return True


def hill_climbing():
    global total_trial
    for trial in range(101):  # Try up to 100 times
        for i in range(8):
            for j in range(8):
                temp[i][j] = queens[i][j]

        h = [[0] * 8 for _ in range(8)]
        min_h = 9999
        min_x, min_y, cur_state = 0, 0, 0

        for i in range(8):
            for j in range(8):
                for k in range(8):
                    temp[i][k] = 0
                h[i][j] = find_collision(i, j)
                if queens[i][j] == 1:
                    cur_state = h[i][j]
                if h[i][j] < min_h:
                    min_h = h[i][j]
                    min_x, min_y = i, j
                for k in range(8):
                    temp[i][k] = queens[i][k]

        if cur_state > min_h:
            for i in range(8):
                queens[min_x][i] = 0
            queens[min_x][min_y] = 1

        if check(h):
            total_trial += trial
            return True

    return False


def first_choose():
    global total_trial
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
        next_x, next_y, times = 0, 0, 0
        while not better:
            next_position = random.randint(0, 63)
            next_x, next_y = next_position // 8, next_position % 8
            next_state = h[next_x][next_y]
            if next_state < cur_state:
                better = True
            if times > 100:
                break
            times += 1

        if better:
            for i in range(8):
                queens[next_x][i] = 0
            queens[next_x][next_y] = 1

        if check(h):
            total_trial += trial
            return True

    return False


def simulated_annealing():
    global total_trial
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
        next_x, next_y, times = 0, 0, 0

        next_position = random.randint(0, 63)
        next_x, next_y = next_position // 8, next_position % 8
        next_state = h[next_x][next_y]
        E = next_state - cur_state
        if E < 0:
            better = True
        elif math.exp((-1) * E / temperature) > (random.random()):
            better = True

        if better:
            for i in range(8):
                queens[next_x][i] = 0
            queens[next_x][next_y] = 1
            trial += 1

        if check(h):
            total_trial += trial
            return True

        temperature *= 0.99

    return False


def steepest_ascent():
    count = 0
    for i in range(1000):
        initial()
        if hill_climbing():
            count += 1
    return count


def first_chose():
    count = 0
    for i in range(1000):
        initial()
        if first_choose():
            count += 1
    return count


def random_restart():
    find_solution = False
    while not find_solution:
        initial()
        find_solution = hill_climbing()
    return find_solution


def main():
    random.seed(time.time())

    global total_trial
    total_trial = 0
    print("Steepest-Ascent searching...")
    count = steepest_ascent()
    print(f"Steepest-Ascent [success/total]: {count}/1000")
    print(f"Average steps: {total_trial / count}")

    # total_trial = 0
    # print("Random-Restart searching...")
    # count2 = random_restart()
    # print(f"Random-Restart: {count2}")
    # print(f"Average steps: {total_trial / count2}")

    # total_trial = 0
    # print("First-Choose searching...")
    # count3 = first_chose()
    # print(f"First-Choose [success/total]: {count3}/1000")
    # print(f"Average steps: {total_trial / count3}")

    # total_trial = 0
    # print("Simulated-Annealing searching...")
    # count4 = simulated_annealing()
    # print(f"Simulated-Annealing [success/total]: {count4}/1000")
    # print(f"Average steps: {total_trial / count4}")


if __name__ == "__main__":
    main()
