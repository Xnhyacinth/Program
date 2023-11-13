import random
import math
import time
import matplotlib.pyplot as plt
# 方向数组：右下左上
direction = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# 当前状态
current = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

# 0的坐标
row_0, col_0 = 0, 0

# 移动步数统计
totalTrial = 0

# 计算曼哈顿距离
def Manhattan():
    sum = 0
    for i in range(3):
        for j in range(3):
            if current[i][j] == 0:
                continue
            row = current[i][j] // 3
            col = current[i][j] % 3
            distance = abs(row - i) + abs(col - j)
            sum += distance
    return sum

# 打印当前状态
def print_state():
    for i in range(3):
        for j in range(3):
            print(current[i][j], end=" ")
        print()
    print()

# 初始化状态
def initialize():
    for i in range(3):
        for j in range(3):
            current[i][j] = i * 3 + j
    global row_0, col_0
    row_0, col_0 = 0, 0
    last = -1

    for m in range(20):
        upset = False
        while not upset:
            dir = random.randint(0, 3)
            if last != -1 and last != dir and abs(last - dir) == 2:
                continue
            x = row_0 + direction[dir][0]
            y = col_0 + direction[dir][1]
            if 0 <= x < 3 and 0 <= y < 3:
                current[row_0][col_0], current[x][y] = current[x][y], current[row_0][col_0]
                row_0, col_0 = x, y
                last = dir
                upset = True

# 判断是否有解
def check():
    for i in range(3):
        for j in range(3):
            if current[i][j] != i * 3 + j:
                return False
    return True

# 爬山法
def hillClimbing():
    global row_0, col_0
    for trial in range(200):
        curManha = Manhattan()
        minMan = 99999
        minX, minY = 0, 0
        for i in range(4):
            x = row_0 + direction[i][0]
            y = col_0 + direction[i][1]
            if 0 <= x < 3 and 0 <= y < 3:
                current[row_0][col_0], current[x][y] = current[x][y], current[row_0][col_0]
                nextManha = Manhattan()
                if nextManha < minMan:
                    minMan = nextManha
                    minX, minY = x, y
                current[x][y], current[row_0][col_0] = current[row_0][col_0], current[x][y]
        if curManha > minMan:
            current[row_0][col_0], current[minX][minY] = current[minX][minY], current[row_0][col_0]
            row_0, col_0 = minX, minY
        if check():
            global totalTrial
            totalTrial += trial
            return True
    return False

# 首选爬山法
def firstChose():
    global row_0, col_0
    for trial in range(500):
        next = False
        times = 0
        while not next:
            dir = random.randint(0, 3)
            curManha = Manhattan()
            x = row_0 + direction[dir][0]
            y = col_0 + direction[dir][1]
            if 0 <= x < 3 and 0 <= y < 3:
                current[row_0][col_0], current[x][y] = current[x][y], current[row_0][col_0]
                nextManha = Manhattan()
                if nextManha < curManha:
                    row_0, col_0 = x, y
                    next = True
                else:
                    current[x][y], current[row_0][col_0] = current[row_0][col_0], current[x][y]
                times += 1
            if times > 20:
                break
        if check():
            global totalTrial
            totalTrial += trial
            return True
    return False

# 模拟退火算法
def simulatedAnnealing():
    global row_0, col_0
    temperature = 5
    trial = 0
    while temperature > 0.00001:
        v = []
        for i in range(4):
            x = row_0 + direction[i][0]
            y = col_0 + direction[i][1]
            if 0 <= x < 3 and 0 <= y < 3:
                v.append(i)
        curManha = Manhattan()
        dir = random.choice(v)
        x = row_0 + direction[dir][0]
        y = col_0 + direction[dir][1]
        current[row_0][col_0], current[x][y] = current[x][y], current[row_0][col_0]
        nextManha = Manhattan()
        E = nextManha - curManha
        if E < 0:
            row_0, col_0 = x, y
            trial += 1
        elif math.exp(-E / temperature) > (random.random()):
            row_0, col_0 = x, y
            trial += 1
        else:
            current[x][y], current[row_0][col_0] = current[row_0][col_0], current[x][y]
        temperature *= 0.999
        if check():
            global totalTrial
            totalTrial += trial
            return True
    return False

# 最陡上升爬山法
def steepestAscent():
    count = 0
    for i in range(1000):
        initialize()
        if hillClimbing():
            count += 1
    return count

# 随机重新开始爬山法
def randomRestart():
    find = False
    while not find:
        initialize()
        find = hillClimbing()
    return find

# 首选爬山法
def firstChoseSearch():
    count = 0
    for i in range(1000):
        initialize()
        if firstChose():
            count += 1
    return count

# 模拟退火搜索
def simulatedAnnealingSearch():
    count = 0
    for i in range(1000):
        initialize()
        if simulatedAnnealing():
            count += 1
    return count

# 绘制性能曲线
def plot_performance_curve(scores_ed, scores_eq):
    
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus']=False
    plt.figure(figsize=(10, 5))
    x = [0, 1, 2, 3]
    # plt.subplot(1, 2, 1)
    # plt.plot(sum(costs[:max_attempts]) / max_attempts, label='Hill Climbing')
    # plt.plot(sum(costs[max_attempts:]) / max_attempts, label='Random Restart Hill Climbing')
    # plt.plot(sum(costs_first_choice) / max_attempts, label='First Choice Hill Climbing')
    # plt.plot(sum(costs_simulated_annealing) / max_attempts, label='Simulated Annealing')
    plt.plot(scores_ed, label='八数码')
    # plt.plot(scores_eq, label='八皇后')
    plt.xticks(x, ['最陡上升爬山法', '首选爬山法', '随机重启爬山法', '模拟退火算法'])
    plt.xlabel("方法")
    plt.ylabel("成功率")
    plt.title("四种方法查找成功率的比较")
    
    plt.plot(scores_eq, label='八皇后')
    for i, prob in enumerate(scores_eq):
        if prob > 0.001:
            plt.text(x[i], prob, f'{prob:.3f}', ha='center', va='bottom')
    for i, prob in enumerate(scores_ed):
        if prob > 0.001:
            plt.text(x[i], prob, f'{prob:.3f}', ha='center', va='bottom')
    # plt.subplot(1, 2, 2)
    # a = [sum(success_rates[:max_attempts]) / max_attempts]
    # a.append(sum(success_rates[max_attempts:]) / max_attempts)
    # a.append(sum(success_rates_first_choice) / max_attempts)
    # a.append(sum(success_rates_simulated_annealing) / max_attempts)
    # plt.plot(a, label='Simulated Annealing')
    # plt.plot(sum(success_rates[:max_attempts]) / max_attempts, label='Hill Climbing')
    # plt.plot(sum(success_rates[max_attempts:]) / max_attempts, label='Random Restart Hill Climbing')
    # plt.plot(sum(success_rates_first_choice) / max_attempts, label='First Choice Hill Climbing')
    # plt.plot(sum(success_rates_simulated_annealing) / max_attempts, label='Simulated Annealing')
    plt.legend()
    # plt.xlabel("Attempts")
    # plt.ylabel("Success Rate")
    # plt.title(f"Success Rate vs. Attempts (Max Attempts = {max_attempts})")
    plt.savefig('a.png')

if __name__ == "__main__":
    # random.seed(time.time())
    # totalTrial = 0
    # scores = []
    # print("Steepest-Ascent searching...")
    # count = steepestAscent()
    # print(f"Steepest-Ascent [success/total]: {count}/1000")
    # print(f"Average steps: {totalTrial / count}")
    # scores.append(count/1000)
    # totalTrial = 0
    # print("Random-Restart searching...")
    # count2 = randomRestart()
    # print(f"Random-Restart: {count2}")
    # print(f"Average steps: {totalTrial / count2}")
    # scores.append(count2)
    # totalTrial = 0
    # print("First-Chose searching...")
    # count3 = firstChoseSearch()
    # print(f"First-Chose [success/total]: {count3}/1000")
    # print(f"Average steps: {totalTrial / count3}")
    # scores.append(count3/1000)
    # totalTrial = 0
    # print("Simulated-Annealing searching...")
    # count4 = simulatedAnnealingSearch()
    # print(f"Simulated-Annealing [success/total]: {count4}/1000")
    # print(f"Average steps: {totalTrial / count4}")
    # scores.append(count4/1000)
    ##[8.560140371322632, 9.35342264175415, 1351.625123500824, 3887.748220205307]
# [949, 966, 935, 901]
    scores = [0.037, 0.037, 0.486, 0.318]
    plot_performance_curve(scores, [0.949, 0.966, 0.935, 0.901])
