## The Eight Queens and the Eight Digits Problem

### Define
Generate a large number of 8-puzzle and 8-queens instances and solve them(where possible) by hill climbing (steepest-ascent and first-choice variants), hill climbing with random restart, and simulated annealing. Measure the search cost and percentage of solved problems and graph these against the optimal solution cost. Comment on your results.

生成大量的八数码问题和八皇后问题并用以下算法分别求解：爬山法（最陡上升和首选爬山法），随机重启爬山法，模拟退火算法。计算搜索耗散和问题的解决率，并用图对比它们的最优解代价的曲线。对结果进行评估。

### 八皇后

![img](https://s2.loli.net/2023/11/13/CeNZRufMBjYlFo3.png)

上图的表示方法为：board[5,0,4,2,8,2,7,3]

#### 随机生成一千个实例写入文件

```python
import random
def main():
    f = open("eightQueensTest.txt", "wb")
    testCaseCount = 1000
    board = ""
    while testCaseCount > 0:
        testCaseCount -= 1
        for col in range(0,7):
            board += str(random.randint(0,7)) + ' '
        board += str(random.randint(0,7)) + '\n'
    f.write(board)
    f.close()
    
if __name__ == '__main__':
    main()
```

#### 在每种方法的主函数中读文件获得实例并调用方法求解问题

#### 启发式代价

用互相攻击的皇后数表示

![img](https://s2.loli.net/2023/11/13/oH5FVYZgh4tyzIk.png)

```python
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
```

### 八数码

![img](https://s2.loli.net/2023/11/13/qnof4AUxbpXzOLJ.png)

上图是目标状态，0表示空白方块，其他数字可以移动到该位置。代码中用board[0,1,2,3,4,5,6,7,8]来表示

随机生成一千个实例写入文件

从目标状态开始，随机移动空白块一定次数（如5000次）生成实例来确保有解

#### 启发式代价
每个数码到目标位置的曼哈顿距离之和，为0时找到解

```python
# heuristic cost
# manhattan_distance
def getManhattanDistance(board):
    distance = 0
    for i in range(len(board)):
        distance += abs(i/3 - board[i]/3) + abs(i%3 - board[i]%3)
    return distance
```

### 结果对比

最陡上升爬山法计算当前棋盘所有空位置（该列的皇后挪动到该行）的启发式代价（互相攻击皇后数），选择代价最低的。

首选爬山法随机选择一个空位置，若该位置优于当前棋盘，则选择之。

随机重启爬山法随机选择一个空位置。

模拟退火算法结合了爬山法，随机选一个空位置，若冲突数更小，则移动到那里。反之，以一定概率接受更差的选择，避免高不成低不就。

每种方法的预期能找到解或失败的循环次数和方法相关。例如最陡上升爬山法有找到解和达到局部最优解或平原地带而陷入循环两种状态。通过测试，200步是合理的预期步数。而模拟退火算法经测试通常在万步级（几万/几十万步）找到解，具体来说是500000步内，不排除超出的情况，处于时间考虑，将超出50万步的视为失败。

对一千个随机生成的样例进行测试并对比结果如下

#### 成功率比较

![image-20231113131827165](https://s2.loli.net/2023/11/13/Vb9HLmBP1oN5Kav.png)

#### 搜索耗散比较

![image-20231113131746574](https://s2.loli.net/2023/11/13/taI5r8bLiXJhMS6.png)


数据显示，四种方法对于八皇后问题的解决率都在90%以上，差距不明显。首选爬山法相对较优，模拟退火算法相对较劣。而时间上差距悬殊，最陡上升爬山法和首选爬山法用时极少，随机重启爬山法和模拟退火算法用时极多。相对快的首选爬山法比相对慢的模拟退火算法快了约六百倍。综合来看，首选爬山法最优，最陡上升爬山法稍次之，另两种方法在时间上可以淘汰了。

而八数码问题时间上和八皇后问题态势接近，解决率却大相径庭。随机重启爬山法和模拟退火算法的解决率不到百分之五十，原来高高在上的最陡上升爬山法和首选爬山法的解决率很低。

八皇后问题一个棋盘有`8*8-8=56`个随机选择，八皇后问题在不考虑旋转与翻转等价时,共有92 个不同的解，考虑时解更多，因此比当前棋盘更优的选择不会少。每次都能减少一点冲突，很快就能成功解决。

八数码问题一个棋盘的随机选择数在2到4之间，比当前棋盘更优的选择寥寥。经试验，大量棋盘会卡在局部最优解（局部顶峰/平原）而被判失败。