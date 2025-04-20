import os
import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                "/../../../MotionPlanning/")

import CurvesGenerator.reeds_shepp as rs

MAX_STEER = 8.0/15  # [rad] maximum steering angle
WB = 2.716  # [m] Wheel base
MOVE_STEP = 0.4  # [m] path interporate resolution

# 起点与终点 (x, y, yaw in rad)
start = (2.0, 2.0, np.deg2rad(0))
goal = (2.0, 2.5, np.deg2rad(0))

maxc = math.tan(MAX_STEER) / WB     # 最大曲率

paths = rs.calc_all_paths(start[0], start[1], start[2], goal[0], goal[1], goal[2], 
                          maxc, step_size=MOVE_STEP) # MOVE_STEP = 0.4

print(len(paths))
fig, axes = plt.subplots(1, len(paths), figsize=(5 * len(paths), 5))

for i, (path, ax) in enumerate(zip(paths, axes)):
    xs = path.x
    ys = path.y
    # color = [random.random() for _ in range(3)]
    ax.plot(xs, ys, marker='o')

    dx = np.cos(start[2]) * 0.5  # 箭头长度 * 方向
    dy = np.sin(start[2]) * 0.5
    ax.arrow(start[0], start[1], dx, dy, head_width=0.2, head_length=0.3, fc='red', ec='red')

    dx = np.cos(goal[2]) * 0.5  # 箭头长度 * 方向
    dy = np.sin(goal[2]) * 0.5
    ax.arrow(goal[0], goal[1], dx, dy, head_width=0.2, head_length=0.3, fc='red', ec='red')

    ax.set_title(f'Path {i+1}')
    ax.set_aspect('equal')
    ax.grid(True)


# plt.plot(start[0], start[1], 'go', label="Start")
# plt.plot(goal[0], goal[1], 'ro', label="Goal")
plt.tight_layout()
plt.show()


