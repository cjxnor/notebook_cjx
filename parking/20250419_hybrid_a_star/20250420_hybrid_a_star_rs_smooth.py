import numpy as np
import matplotlib.pyplot as plt
import reeds_shepp

# 车辆参数
turning_radius = 1.0
step_size = 0.2

# 起点与终点 (x, y, yaw in rad)
start = (2.0, 2.0, np.deg2rad(0))
goal = (8.0, 6.0, np.deg2rad(180))

# 使用 path_sample 获取路径
path = reeds_shepp.path_sample(start, goal, turning_radius, step_size)

# 六边形车辆轮廓
def get_hexagon(x, y, yaw, length=2.5):
    angles = np.linspace(0, 2 * np.pi, 6, endpoint=False)
    offset_x = (length / 2) * np.cos(angles)
    offset_y = (length / 2) * np.sin(angles)
    rot = np.array([[np.cos(yaw), -np.sin(yaw)],
                    [np.sin(yaw),  np.cos(yaw)]])
    points = np.dot(rot, np.vstack((offset_x, offset_y)))
    return x + points[0], y + points[1]

# 障碍物和车位
obstacles = [(5, 3, 6, 7)]
parking_slot = (7.5, 5.5, 8.5, 6.5)

# 可视化
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.set_title("Reeds-Shepp Parking (path_sample version)")

# 画障碍物
for (x1, y1, x2, y2) in obstacles:
    ax.fill([x1, x2, x2, x1], [y1, y1, y2, y2], color='gray', label='Obstacle')

# 画车位
px1, py1, px2, py2 = parking_slot
ax.plot([px1, px2, px2, px1, px1], [py1, py1, py2, py2, py1], 'g--', label='Parking Slot')

# 画路径 + 六边形车辆
for i, (x, y, yaw, *_ ) in enumerate(path):
    if i % 5 == 0:
        hx, hy = get_hexagon(x, y, yaw)
        ax.fill(hx, hy, color='orange', alpha=0.4)
    ax.plot(x, y, 'b.', markersize=2)

# 起点终点
ax.plot(start[0], start[1], 'go', label='Start')
ax.plot(goal[0], goal[1], 'ro', label='Goal')
ax.legend()
plt.grid(True)
plt.show()
