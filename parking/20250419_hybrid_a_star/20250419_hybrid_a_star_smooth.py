import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.interpolate import splprep, splev
import heapq

# ========== 环境配置 ==========
obstacles = [
    (4, 4, 6, 6),   # 障碍物：矩形 (x1, y1, x2, y2)
    (7, 2, 9, 3.5)
]
car_width = 1.8
car_length = 4.0

start = (1, 1, 0)
goal = (8, 8, 90)
map_size = (10, 10)
resolutions = [1.0, 0.5]  # 可变分辨率

# ========== 状态扩展函数 ==========
def get_neighbors(x, y, theta, res):
    actions = [(1, 0), (-1, 0), (1, 30), (1, -30), (-1, 30), (-1, -30)]
    neighbors = []
    for forward, steer in actions:
        new_theta = (theta + steer) % 360
        rad = np.deg2rad(new_theta)
        dx = forward * np.cos(rad) * res
        dy = forward * np.sin(rad) * res
        new_x, new_y = x + dx, y + dy
        neighbors.append((new_x, new_y, new_theta))
    return neighbors

# ========== 碰撞检测 ==========
def is_collision(x, y):
    for ox1, oy1, ox2, oy2 in obstacles:
        if ox1 <= x <= ox2 and oy1 <= y <= oy2:
            return True
    if not (0 <= x <= map_size[0] and 0 <= y <= map_size[1]):
        return True
    return False

# ========== Hybrid A* 主体 ==========
def hybrid_astar(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    cost_so_far = {start: 0}
    visited = []

    while open_set:
        _, current = heapq.heappop(open_set)
        visited.append(current)

        if np.hypot(current[0] - goal[0], current[1] - goal[1]) < 0.8:
            break

        res = resolutions[0] if len(visited) < 100 else resolutions[1]

        for neighbor in get_neighbors(*current, res):
            if is_collision(neighbor[0], neighbor[1]):
                continue
            new_cost = cost_so_far[current] + res
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + np.hypot(neighbor[0] - goal[0], neighbor[1] - goal[1])
                heapq.heappush(open_set, (priority, neighbor))
                came_from[neighbor] = current

    # 回溯路径
    path = []
    node = current
    while node != start:
        path.append(node)
        node = came_from.get(node, start)
    path.append(start)
    path.reverse()
    return path, visited

# ========== 路径平滑 ==========
# 使用b样条曲线平滑，并没有考虑车辆的曲率约束
def smooth_path(path):
    # (x,y,theta)
    x, y = zip(*[(p[0], p[1]) for p in path])
    # splprep是 将离散的点拟合成平滑的 B 样条曲线（B-spline）。它会返回一个参数化的样条函数
    # s是平滑因子，越小越贴近原始点，越大越平滑，s=0 表示严格穿过所有点
    tck, u = splprep([x, y], s=1)
    u_fine = np.linspace(0, 1, 200)
    # splev用来评估（evaluate）由 splprep 拟合出来的样条曲线，根据给定的参数 u，得到曲线上的点
    # 得到拟合曲线上 200 个点
    x_fine, y_fine = splev(u_fine, tck)
    dx = np.gradient(x_fine)
    dy = np.gradient(y_fine)
    theta_fine = np.arctan2(dy, dx)
    return x_fine, y_fine, theta_fine

# ========== 动画 ==========
def animate_search(path, visited, smoothed):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(0, map_size[0])
    ax.set_ylim(0, map_size[1])
    ax.set_aspect('equal')
    ax.set_title("Hybrid A* with Path Smoothing")

    # 绘制障碍物
    for ox1, oy1, ox2, oy2 in obstacles:
        ax.fill([ox1, ox2, ox2, ox1], [oy1, oy1, oy2, oy2], 'gray')

    visited_scatter, = ax.plot([], [], 'c.', alpha=0.3, label="Visited")
    path_line, = ax.plot([], [], 'r-', lw=2, label="Raw Path")
    smooth_line, = ax.plot([], [], 'b-', lw=2, label="Smoothed")
    arrows = []

    def init():
        visited_scatter.set_data([], [])
        path_line.set_data([], [])
        smooth_line.set_data([], [])
        return visited_scatter, path_line, smooth_line

    def update(frame):
        if frame < len(visited):
            vx, vy = zip(*[(v[0], v[1]) for v in visited[:frame+1]])
            visited_scatter.set_data(vx, vy)
        elif frame < len(visited) + len(path):
            px, py = zip(*[(p[0], p[1]) for p in path[:frame - len(visited) + 1]])
            path_line.set_data(px, py)
        else:
            s_idx = frame - len(visited) - len(path)
            smooth_line.set_data(smoothed[0][:s_idx], smoothed[1][:s_idx])
            for arrow in arrows:
                arrow.remove()
            arrows.clear()
            for i in range(0, s_idx, 10):
                x, y = smoothed[0][i], smoothed[1][i]
                dx, dy = np.cos(smoothed[2][i]), np.sin(smoothed[2][i])
                arrow = ax.arrow(x, y, dx * 0.5, dy * 0.5, head_width=0.2, color='green')
                arrows.append(arrow)
        return visited_scatter, path_line, smooth_line, *arrows

    total_frames = len(visited) + len(path) + len(smoothed[0])
    ani = FuncAnimation(fig, update, frames=total_frames, init_func=init, blit=False, interval=30, repeat=False)
    ax.legend()
    plt.show()

# ========== 主程序 ==========
path, visited = hybrid_astar(start, goal)
smoothed = smooth_path(path)
animate_search(path, visited, smoothed)
