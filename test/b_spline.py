import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline

# 设定控制点（coefficients），影响 B 样条曲线的形状
control_points = np.array([0, 1, 2, 1, 0, -1, -2, -1, 0])

# 设定阶数（degree）
degree = 5  # 5 次 B 样条

# 计算所需的节点数量：n_knots = n_control_points + degree + 1
n_knots = len(control_points) + degree + 1

# 生成节点向量（knots）
knots = np.concatenate(([0] * degree, np.linspace(0, 1, n_knots - 2 * degree), [1] * degree))

# 创建 B 样条曲线
spl = BSpline(knots, control_points, degree)

# 生成曲线的 x 轴数据
x = np.linspace(0, 1, 200)  # 200 个采样点
y = spl(x)  # 计算曲线上的 y 值

# 绘制 B 样条曲线
plt.plot(x, y, label="5th-degree B-Spline Curve", linewidth=2, color="blue")

# 绘制控制点
control_x = np.linspace(0, 1, len(control_points))  # 控制点的 x 坐标
plt.scatter(control_x, control_points, color='red', label="Control Points", zorder=3)

# 添加图例和标题
plt.title("5th-degree B-Spline Curve")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)

# 显示图像
plt.show()
