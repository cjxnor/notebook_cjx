# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

def rotate_around_point(point, angle, center):
    """绕指定点 center 旋转二维点"""
    theta = np.radians(angle)
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                [np.sin(theta), np.cos(theta)]])
    
    # 平移点到原点 -> 旋转 -> 平移回去
    translated_point = point - center
    rotated_point = np.dot(rotation_matrix, translated_point)
    return rotated_point + center

# 示例
point = np.array([2, 2])  # 旋转点
center = np.array([1, 1])  # 旋转中心
angle = 90
new_point = rotate_around_point(point, angle, center)
print(new_point)  # 输出: [0. 2.]


# 生成点
point = np.array([2, 1])
center = np.array([1, 1])
angle = 90

# 旋转
new_point = rotate_around_point(point, angle, center)

# 绘制
plt.figure(figsize=(5, 5))
plt.scatter(*point, color='red', label='Original Point')
plt.scatter(*new_point, color='blue', label='Rotated Point')
plt.scatter(*center, color='green', label='Center')
plt.plot([point[0], new_point[0]], [point[1], new_point[1]], 'k--')  # 连接线
plt.xlim(-1, 3)
plt.ylim(-1, 3)
plt.grid()
plt.legend()
plt.show()
