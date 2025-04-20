import numpy as np
import matplotlib.pyplot as plt
import reeds_shepp

# 车辆参数
turning_radius = 5.0
step_size = 0.2

# 起点与终点 (x, y, yaw in rad)
start = (2.0, 2.0, np.deg2rad(0))
goal = (8.0, 6.0, np.deg2rad(180))

# 使用 path_sample 获取路径
path = reeds_shepp.path_sample(start, goal, turning_radius, step_size)

# 可视化
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-5, 10)
ax.set_ylim(-5, 10)
ax.set_aspect('equal')
ax.set_title("Reeds-Shepp Parking (path_sample version)")

# 画路径
for i, (x, y, yaw, *_ ) in enumerate(path):
    ax.plot(x, y, 'b.', markersize=2)

# 起点终点
ax.plot(start[0], start[1], 'go', label='Start')
ax.plot(goal[0], goal[1], 'ro', label='Goal')
ax.legend()
plt.grid(True)
plt.show()
