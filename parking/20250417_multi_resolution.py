import numpy as np
import matplotlib.pyplot as plt
import heapq

# 配置地图参数
COARSE_RES = 1.0
FINE_RES = 0.25
MAP_SIZE = 20

# 定义障碍物和终点
obstacles = [(5, y) for y in range(5, 15)] + [(x, 10) for x in range(6, 15)]
goal = (17, 17)
start = (2, 2)

# 判断是否使用 finer grid
def is_fine_grid(x, y):
    gx, gy = goal
    return abs(x - gx) < 3 and abs(y - gy) < 3

# A* 核心实现
def astar(start, goal, get_neighbors, heuristic):
    open_set = []
    # 把三元组 (f, g, node) 推入了 open_set
    # heapq 会根据 第一个元素（f 值） 来自动排序，保证最小 f 的节点最先弹出
    heapq.heappush(open_set, (0 + heuristic(start), 0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while open_set:
        _, cost, current = heapq.heappop(open_set)

        if current == goal:
            break

        for neighbor in get_neighbors(current):
            new_cost = cost + np.linalg.norm(np.array(current) - np.array(neighbor))
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor)
                heapq.heappush(open_set, (priority, new_cost, neighbor))
                came_from[neighbor] = current

    # 回溯路径
    path = []
    node = goal
    while node in came_from:
        path.append(node)
        node = came_from[node]
    path.append(start)
    path.reverse()
    return path

# 获取邻居（根据当前分辨率）
def get_neighbors(pos):
    x, y = pos
    res = FINE_RES if is_fine_grid(x, y) else COARSE_RES
    steps = [(-res, 0), (res, 0), (0, -res), (0, res)]
    neighbors = []
    for dx, dy in steps:
        # round()用于保留2位小数
        nx, ny = round(x + dx, 2), round(y + dy, 2)
        if 0 <= nx < MAP_SIZE and 0 <= ny < MAP_SIZE and (int(nx), int(ny)) not in obstacles:
            neighbors.append((nx, ny))
    return neighbors

# 启发函数
def heuristic(p):
    # 计算L2范数
    return np.linalg.norm(np.array(p) - np.array(goal))

# 执行 A* 搜索
path = astar(start, goal, get_neighbors, heuristic)

# 可视化
def plot_map():
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # 画粗栅格
    for x in range(MAP_SIZE + 1):
        # 画一条竖直线，X坐标从x到x，Y坐标从0到MAP_SIZE
        ax.plot([x, x], [0, MAP_SIZE], color='lightgray', linewidth=0.5)
    for y in range(MAP_SIZE + 1):
        ax.plot([0, MAP_SIZE], [y, y], color='lightgray', linewidth=0.5)

    # 画障碍
    for ox, oy in obstacles:
        # ox,oy是左下角坐标，1，1是宽高
        ax.add_patch(plt.Rectangle((ox, oy), 1, 1, color='black'))

    # 画路径
    if path:
        # path是list，*path 是 Python 的 解包（unpacking）语法，意思是：把列表里的元素一个个拿出来传给函数
        px, py = zip(*path)
        ax.plot(px, py, color='green', linewidth=2, label='Path')

    # 起点终点
    # start是一个元组，*start 表示：把这个元组“拆开”，一个一个地传进去
    ax.plot(*start, 'bo', label='Start')
    ax.plot(*goal, 'ro', label='Goal')

    ax.set_xlim(0, MAP_SIZE)
    ax.set_ylim(0, MAP_SIZE)
    # 让 x 轴和 y 轴的刻度长度“相等”
    ax.set_aspect('equal')
    ax.grid(False)
    ax.legend()
    plt.title("Multi-Resolution Grid A* Path Planning")
    plt.show()

plot_map()
