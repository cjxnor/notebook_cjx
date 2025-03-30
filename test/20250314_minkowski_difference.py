import numpy as np
import matplotlib.pyplot as plt

def minkowski_difference(shape1, shape2):
    """计算两个 2D 形状的 Minkowski 差"""
    diff_points = []
    for p1 in shape1:
        for p2 in shape2:
            diff_points.append(np.array(p1) - np.array(p2))
    return np.array(diff_points)

# 定义两个 2D 形状
shape1 = np.array([[0,0], [2,0], [1,2]])  # 三角形
shape2 = np.array([[1,1], [3,1], [3,3], [1,3]])  # 矩形

# 计算 Minkowski 差
diff = minkowski_difference(shape1, shape2)

# 画出原始形状和 Minkowski 差
plt.figure(figsize=(8,4))
plt.subplot(1,2,1)
plt.fill(*zip(*shape1), 'r', alpha=0.5, label="Shape A")
plt.fill(*zip(*shape2), 'b', alpha=0.5, label="Shape B")
plt.legend()
plt.title("Original Shapes")

plt.subplot(1,2,2)
plt.scatter(diff[:,0], diff[:,1], color='g', alpha=0.5)
plt.axhline(0, color='k', linestyle='--')
plt.axvline(0, color='k', linestyle='--')
plt.title("Minkowski Difference")
plt.show()
