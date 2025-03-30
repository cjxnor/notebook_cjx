# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange

# 已知数据点
x_points = np.array([1, 3, 4])
y_points = np.array([2, 6, 5])

# 使用 scipy 计算 Lagrange 插值多项式
poly = lagrange(x_points, y_points)

# 生成插值曲线
x_new = np.linspace(0, 5, 100)
y_new = poly(x_new)

# 画图
plt.plot(x_points, y_points, 'ro', label="数据点")
plt.plot(x_new, y_new, 'b-', label="Lagrange 插值多项式")
plt.legend()
plt.show()
