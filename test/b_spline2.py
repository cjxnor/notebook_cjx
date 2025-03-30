import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline

# 初始控制点
control_points = np.array([[0, 0], [1, 2], [2, 1], [3, -1], [4, -2], [5, 1], [6, 2], [7, 0]])

# 阶数（5 次 B 样条）
degree = 5

# 计算所需的节点数量
n_knots = len(control_points) + degree + 1

# 生成均匀分布的节点向量
knots = np.concatenate(([0] * degree, np.linspace(0, 1, n_knots - 2 * degree), [1] * degree))

# 记录被拖动的点索引
dragging_index = None

# 初始化图像
fig, ax = plt.subplots()
ax.set_title("Interactive 5th-degree B-Spline")
ax.set_xlim(-1, 8)
ax.set_ylim(-3, 3)
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.grid(True)

# 绘制初始 B 样条曲线
def update_bspline():
    global spline_curve, control_scatter
    # 计算 B 样条曲线
    spl = BSpline(knots, control_points[:, 1], degree)
    x_vals = np.linspace(0, 1, 200)
    y_vals = spl(x_vals)
    
    # 映射 x 轴到控制点范围
    x_mapped = np.linspace(control_points[:, 0].min(), control_points[:, 0].max(), len(x_vals))
    
    # 更新曲线
    spline_curve.set_data(x_mapped, y_vals)
    control_scatter.set_offsets(control_points)

# 绘制控制点和 B 样条曲线
spline_curve, = ax.plot([], [], 'b-', linewidth=2, label="B-Spline Curve")
control_scatter = ax.scatter(control_points[:, 0], control_points[:, 1], color='red', s=100, label="Control Points", picker=True)

update_bspline()
ax.legend()

# 鼠标按下时检测是否选中控制点
def on_press(event):
    global dragging_index
    if event.inaxes is not None:
        distances = np.sqrt((control_points[:, 0] - event.xdata) ** 2 + (control_points[:, 1] - event.ydata) ** 2)
        if np.min(distances) < 0.3:  # 选择最近的点
            dragging_index = np.argmin(distances)

# 鼠标移动时更新控制点位置
def on_motion(event):
    global dragging_index
    if dragging_index is not None and event.inaxes is not None:
        control_points[dragging_index] = [event.xdata, event.ydata]
        update_bspline()
        fig.canvas.draw_idle()

# 鼠标释放时停止拖动
def on_release(event):
    global dragging_index
    dragging_index = None

# 绑定鼠标事件
fig.canvas.mpl_connect("button_press_event", on_press)
fig.canvas.mpl_connect("motion_notify_event", on_motion)
fig.canvas.mpl_connect("button_release_event", on_release)

# 显示交互式图像
plt.show()
