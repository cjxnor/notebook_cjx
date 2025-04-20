import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import heapq

# === 配置参数 ===
COARSE_RES = 1.0
FINE_RES = 0.25
MAP_SIZE = 20
goal = (17, 17)
start = (2, 2)

# 定义障碍物
obstacles = {(5, y) for y in range(5, 15)} | {(x, 10) for x in range(6, 15)}

# 判断是否使用 finer grid
def is_fine_grid(x, y):
    gx, gy = goal
    return abs(x - gx) < 3 and abs(y - gy) < 3

# 启发函数
def heuristic(p):
    return np.linalg.norm(np.array(p) - np.array(goal))

# 获取邻居节点
def get_neighbors(pos):
    x, y = pos
    res = FINE_RES if is_fine_grid(x, y) else COARSE_RES
    steps = [(-res, 0), (res, 0), (0, -res), (0, res)]
    neighbors = []
    for dx, dy in steps:
        nx, ny = round(x + dx, 2), round(y + dy, 2)
        if 0 <= nx < MAP_SIZE and 0 <= ny < MAP_SIZE and (int(nx), int(ny)) not in obstacles:
            neighbors.append((nx, ny))
    return neighbors

# A* 搜索 + 动画记录
def astar_with_animation(start, goal):
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start), 0, start))
    came_from = {}
    cost_so_far = {start: 0}
    visited_nodes = []

    while open_set:
        _, cost, current = heapq.heappop(open_set)
        visited_nodes.append(current)

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
    return path, visited_nodes

# === 执行 A* 并获取路径和访问节点 ===
path, visited_nodes = astar_with_animation(start, goal)

# === 可视化动画 ===
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, MAP_SIZE)
ax.set_ylim(0, MAP_SIZE)
ax.set_aspect('equal')
ax.set_title("Multi-Resolution Grid A* Path Planning (Animated)")

# 绘制地图（静态部分）
for x in range(MAP_SIZE):
    for y in range(MAP_SIZE):
        if is_fine_grid(x, y):
            ax.add_patch(plt.Rectangle((x, y), FINE_RES, FINE_RES, edgecolor='lightgray', facecolor='white', linewidth=0.2))

# 障碍物
for ox, oy in obstacles:
    ax.add_patch(plt.Rectangle((ox, oy), 1, 1, color='black'))

# 起点终点
ax.plot(*start, 'bo', label='Start')
ax.plot(*goal, 'ro', label='Goal')

# 动画元素
# 创建一个“空点图”—— 没有任何点，先占个位，之后可以动态添加点，'o'：画圆点（marker）
# markersize=3：点的大小为 3
# ax.plot() 返回的是列表，visited_plot, = ax.plot()相当于visited_plot = ax.plot(...)[0]
visited_plot, = ax.plot([], [], 'o', color='orange', markersize=3, label='Visited')
path_plot, = ax.plot([], [], color='green', linewidth=2, label='Path')

def init():
    visited_plot.set_data([], [])
    path_plot.set_data([], [])
    return visited_plot, path_plot

# update(frame) 是 FuncAnimation 每一帧都调用一次的函数，
# 用来根据当前帧数 frame 更新图上的数据（比如已访问节点、最终路径等）
def update(frame):
    if frame < len(visited_nodes):
        # 截取前frame个访问节点
        nodes = visited_nodes[:frame]
        if nodes:  # 防止空列表解包出错
            vx, vy = zip(*nodes)
            visited_plot.set_data(vx, vy)
    else:
        if path:  # 同样防止路径为空时报错
            px, py = zip(*path)
            path_plot.set_data(px, py)
    return visited_plot, path_plot


ani = animation.FuncAnimation(fig, update, frames=len(visited_nodes) + 30,
                              init_func=init, interval=30, blit=True, repeat=False)

ax.legend()
plt.show()
