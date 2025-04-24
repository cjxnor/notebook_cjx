import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

# 参数
radius = 5
car_length = 1.0
car_width = 0.5
omega = 0.5
center = (0, 0)
fps = 30
total_time = 10

# 车辆轮廓
def get_car_corners(x, y, theta):
    dx = car_length / 2
    dy = car_width / 2
    corners = np.array([
        [dx, dy], [dx, -dy],
        [-dx, -dy], [-dx, dy]
    ])
    rot = np.array([[np.cos(theta), -np.sin(theta)],
                    [np.sin(theta),  np.cos(theta)]])
    return corners @ rot.T + np.array([x, y])

# 初始化 Tkinter 窗口
root = tk.Tk()
root.title("车辆轨迹动画（Tkinter 版本）")

# matplotlib figure
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-radius - 2, radius + 2)
ax.set_ylim(-radius - 2, radius + 2)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 图形元素
car_patch = Polygon(np.zeros((4, 2)), closed=True, fc='steelblue', alpha=0.9)
ax.add_patch(car_patch)

arrow = FancyArrowPatch((0, 0), (0.001, 0.001), color='orange', arrowstyle='->', mutation_scale=15)
ax.add_patch(arrow)

trajectory, = ax.plot([], [], 'r--', linewidth=1)
x_traj, y_traj = [], []
show_trajectory = tk.BooleanVar(value=True)

# 控制面板
control_frame = tk.Frame(root)
control_frame.pack(side=tk.RIGHT, fill=tk.Y)

check = tk.Checkbutton(control_frame, text="显示轨迹", variable=show_trajectory)
check.pack(pady=10)

# 动画更新函数
def update(frame):
    t = frame / fps
    angle = omega * t
    x = center[0] + radius * np.cos(angle)
    y = center[1] + radius * np.sin(angle)
    theta = angle + np.pi / 2

    car_patch.set_xy(get_car_corners(x, y, theta))
    arrow.set_positions((x, y), (x + 0.7 * np.cos(theta), y + 0.7 * np.sin(theta)))

    if show_trajectory.get():
        x_traj.append(x)
        y_traj.append(y)
        trajectory.set_data(x_traj, y_traj)
    else:
        trajectory.set_data([], [])

    return car_patch, arrow, trajectory

# 动画对象
anim = FuncAnimation(fig, update, frames=int(total_time * fps), interval=1000/fps, blit=False, repeat=False)

# 启动
root.mainloop()
