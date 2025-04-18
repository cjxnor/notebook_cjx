import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import heapq

# === 配置参数 ===
COARSE_RES = 1.0  # 粗分辨率
FINE_RES = 0.25   # 细分辨率
MAP_SIZE = 20     # 地图尺寸
GOAL_RADIUS = 3   # 终点附近细化范围
MAX_STEERING = 30 # 最大转角

# === 初始状态 ===
start = (2, 2, 0)  # 起点 (x, y, θ)
goal = (16, 16, 90)  # 终点 (x, y, θ)

# 障碍物
obstacles = {(5, y) for y in range(5, 15)} | {(x, 10) for x in range(6, 15)}

# 车辆控制动作（前进1m、后退1m、转 +30°、转 -30°）
actions = [(1, 0), (-1, 0), (0, 30), (0, -30)]  # 前进1m、后退1m、转 +30°、转 -30°

# 判断是否细化栅格
def is_fine_grid(x, y):
    gx, gy, _ = goal
    return abs(x - gx) < GOAL_RADIUS and abs(y - gy) < GOAL_RADIUS

# 计算启发函数（欧几里得距离）
def heuristic(state):
    x, y, _ = state
    gx, gy, _ = goal
    return np.linalg.norm(np.array([x, y]) - np.array([gx, gy]))

# 获取邻居节点（包括控制动作）
def get_neighbors(state):
    x, y, theta = state
    res = FINE_RES if is_fine_grid(x, y) else COARSE_RES
    neighbors = []

    for forward, steer in actions:
        new_theta = (theta + steer) % 360
        rad = np.deg2rad(new_theta)
        dx = forward * np.cos(rad) * res
        dy = forward * np.sin(rad) * res
        new_x, new_y = x + dx, y + dy

        # 确保不越界和不碰撞
        if 0 <= new_x < MAP_SIZE and 0 <= new_y < MAP_SIZE and (int(new_x), int(new_y)) not in obstacles:
            neighbors.append((new_x, new_y, new_theta))

    return neighbors

# Hybrid A* 搜索算法
def hybrid_astar(start, goal):
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start), 0, start))
    came_from = {}
    cost_so_far = {start: 0}
    visited_nodes = []

    while open_set:
        _, cost, current = heapq.heappop(open_set)
        visited_nodes.append(current)

        if abs(current[0] - goal[0]) < 0.5 and abs(current[1] - goal[1]) < 0.5:  # 到达目标位置
            break

        for neighbor in get_neighbors(current):
            new_cost = cost + np.linalg.norm(np.array(current[:2]) - np.array(neighbor[:2]))
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

# === 执行 Hybrid A* 并获取路径和访问节点 ===
path, visited_nodes = hybrid_astar(start, goal)

# === 可视化动画 ===
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, MAP_SIZE)
ax.set_ylim(0, MAP_SIZE)
ax.set_aspect('equal')
ax.set_title("Hybrid A* Path Planning (Animated)")

# 绘制地图（静态部分）
for x in range(MAP_SIZE):
    for y in range(MAP_SIZE):
        if is_fine_grid(x, y):
            ax.add_patch(plt.Rectangle((x, y), FINE_RES, FINE_RES, edgecolor='lightgray', facecolor='white', linewidth=0.2))

# 障碍物
for ox, oy in obstacles:
    ax.add_patch(plt.Rectangle((ox, oy), 1, 1, color='black'))

# 起点终点
ax.plot(*start[:2], 'bo', label='Start')
ax.plot(*goal[:2], 'ro', label='Goal')

# 动画元素
visited_plot, = ax.plot([], [], 'o', color='orange', markersize=3, label='Visited')
path_plot, = ax.plot([], [], color='green', linewidth=2, label='Path')

def init():
    visited_plot.set_data([], [])
    path_plot.set_data([], [])
    return visited_plot, path_plot

def update(frame):
    if frame < len(visited_nodes):
        nodes = visited_nodes[:frame]
        if nodes:  # 防止空列表解包出错
            vx, vy, _ = zip(*nodes)
            visited_plot.set_data(vx, vy)
    else:
        if path:  # 同样防止路径为空时报错
            px, py, _ = zip(*path)
            path_plot.set_data(px, py)
    return visited_plot, path_plot

ani = animation.FuncAnimation(fig, update, frames=len(visited_nodes) + 30,
                              init_func=init, interval=100, blit=True, repeat=False)

ax.legend()
plt.show()
