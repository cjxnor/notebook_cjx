# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# 生成随机障碍物点
obstacles = np.random.rand(10, 2) * 10  # 10 个障碍物点

# 计算 Voronoi 图
vor = Voronoi(obstacles)

# 绘制 Voronoi 图
fig, ax = plt.subplots(figsize=(6,6))
voronoi_plot_2d(vor, ax=ax, show_vertices=False)

# 标注障碍物点
ax.scatter(obstacles[:,0], obstacles[:,1], color='red', s=50, label="Obstacles")

plt.legend()
plt.title("Voronoi Diagram for Skeleton Path")
plt.show()
