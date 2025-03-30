# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline

# 1. 设定 Hybrid A* 生成的路径点
path_points = np.array([[0, 0], [1, 2], [3, 4], [6, 4], [9, 3]])

# 2. 提取 X, Y 坐标
x = path_points[:, 0]
y = path_points[:, 1]

# 3. 计算 B 样条曲线
degree = 3  # B 样条阶数

# 计算合适的节点向量
knots = np.concatenate((
    np.zeros(degree),            
    np.linspace(0, 1, len(x) - degree + 1),  
    np.ones(degree)
))

# 生成 B 样条曲线
spl_x = BSpline(knots, x, degree)
spl_y = BSpline(knots, y, degree)

# 4. 生成平滑路径
t = np.linspace(0, 1, 100)
smooth_x = spl_x(t)
smooth_y = spl_y(t)

# 5. 画图
plt.plot(x, y, 'ro-', label="Hybrid A* Path")  # 原始路径
plt.plot(smooth_x, smooth_y, 'b-', label="B-Spline Smooth Path")  # 平滑轨迹
plt.legend()
plt.grid()
plt.title("Hybrid A* + B-Spline for Autonomous Parking")
plt.show()
