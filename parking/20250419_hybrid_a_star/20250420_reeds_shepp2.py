import numpy as np
import matplotlib.pyplot as plt
import reeds_shepp

# 车辆参数
turning_radius = 5.0

# 起点与终点 (x, y, yaw in rad)
start = (2.0, 2.0, np.deg2rad(0))
goal = (8.0, 6.0, np.deg2rad(180))

# 使用 path_sample 获取路径
path = reeds_shepp.Path(start, goal, turning_radius)

# 生成路径上的点，间隔长度为 0.1
points = path.sample_many(0.1)

xs, ys, yaws = zip(*points)

plt.plot(xs, ys, 'b-')
plt.plot(start[0], start[1], 'go', label="Start")
plt.plot(goal[0], goal[1], 'ro', label="Goal")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.show()
