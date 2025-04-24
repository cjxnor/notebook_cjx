# -*- coding: utf-8 -*-
# 在20250420_reeds_shepp3.py的基础上增加界面显示

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
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

# 示例 path 数据，每个 path 是一个包含 (x, y) 元组的列表
# paths = [
#     [(0, 0), (1, 2), (2, 3), (3, 5)],
#     [(0, 0), (2, 1), (4, 2), (6, 3)],
#     [(0, 0), (1, -1), (2, -2), (3, -3)]
# ]

class PathViewer:
    def __init__(self, master, paths):
        self.master = master
        self.paths = paths
        self.index = 0

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

        # ctypes
        # self.label_ctypes = tk.Label(master, text="", font=("Arial", 14))
        # self.label_ctypes.pack()
        # 总长
        self.label_L = tk.Label(master, text="", font=("Arial", 14))
        self.label_L.pack()

        self.info_text = tk.Text(master, height=6, width=80, font=("Courier", 10))
        self.info_text.pack()
        # 配置左对齐标签
        self.info_text.tag_configure("left", justify="left")

        self.button = tk.Button(master, text="Next", command=self.plot_next_path)
        self.button.pack()

        # self.max_x = max(x for path in paths for x in path.x)
        # self.min_x = min(x for path in paths for x in path.x)
        # self.max_y = max(y for path in paths for y in path.y)
        # self.min_y = min(y for path in paths for y in path.y)

        self.plot_next_path()  # 初始显示第一条路径

    def plot_next_path(self):
        self.ax.clear()
        path = self.paths[self.index]

        xs = path.x
        ys = path.y
        yaws = path.yaw
        ctypes = path.ctypes
        directions = path.directions
        lengths = path.lengths
        L = path.L

        # 分段绘制路径（根据方向）
        for i in range(len(xs) - 1):
            # x_vals = [xs[i], xs[i + 1]]
            # y_vals = [ys[i], ys[i + 1]]
            x_vals = xs[i]
            y_vals = ys[i]
            color = "red" if directions[i] == -1 else "green"
            self.ax.scatter(x_vals, y_vals, color=color)
        # self.ax.plot(xs, ys, marker='o')

         # 加上 yaw 方向箭头
        # for i in range(len(xs)):
        #     dx = 0.3 * np.cos(yaws[i])
        #     dy = 0.3 * np.sin(yaws[i])
        #     self.ax.arrow(xs[i], ys[i], dx, dy, head_width=0.1, head_length=0.15, fc="green", ec="green")

        max_x = max(x for x in xs)
        min_x = min(x for x in xs)
        max_y = max(y for y in ys)
        min_y = min(y for y in ys)

        dx = np.cos(start[2]) * 0.1 * (max_x - min_x)  # 箭头长度 * 方向
        dy = np.sin(start[2]) * 0.1 * (max_x - min_x)
        hw = 0.05 * (max_y - min_y)
        # hl = 1.5 * hw
        self.ax.arrow(start[0], start[1], dx, dy, head_width=hw, head_length=0.3, 
                      fc='green', ec='green')

        dx = np.cos(goal[2]) * 0.1 * (max_x - min_x)  # 箭头长度 * 方向
        dy = np.sin(goal[2]) * 0.1 * (max_x - min_x)
        self.ax.arrow(goal[0], goal[1], dx, dy, head_width=hw, head_length=0.3, 
                      fc='red', ec='red')

        self.ax.plot(start[0], start[1], 'go', label='Start')
        self.ax.plot(goal[0], goal[1], 'ro', label='Goal')

        # self.ax.set_xlim(xmax=self.max_x, xmin=self.min_x)
        # self.ax.set_ylim(ymax=self.max_y, ymin=self.min_y)
        self.ax.set_title(f"path {self.index}/{len(self.paths) - 1}")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid(True)

        self.canvas.draw()

        # 设置路径描述文字
        # self.label_ctypes.config(text=f"ctypes：{ctypes}")
        # self.label_L.config(text=f"L: {L}")
        type_str = ", ".join(f"{k}:{v:.2f}" for k, v in zip(ctypes, lengths))
        info = (
            f"index: {self.index}\n"
            f"totle length: {L:.2f}\n"
            f"points: (xs: {len(xs)}, ys: {len(ys)}, yaws: {len(yaws)})\n"
            f"ctypes: ({type_str})\n"
            f"start: (x: {start[0]:.2f}, y: {start[1]:.2f}, yaw: {start[2]:.2f})\n"
            f"end: (x: {goal[0]:.2f}, y: {goal[1]:.2f}, yaw: {goal[2]:.2f})\n"
        )

        # 从文本框的第 1 行第 0 个字符开始，一直到最后，把所有内容清空
        # 1.0 表示第 1 行的第 0 个字符（注意 tkinter 的文本位置是 "行.列" 格式）
        # tk.END 表示文本末尾
        self.info_text.delete(1.0, tk.END)
        # 把字符串 info 插入到文本末尾（此时已经清空，所以等于插入到开头）
        self.info_text.insert(tk.END, info, "left")

        self.index = (self.index + 1) % len(self.paths)  # 循环切换

# 监听窗口关闭事件
def on_closing():
    root.quit()  # 停止 Tkinter 主循环，确保脚本退出
    root.destroy()  # 彻底销毁窗口

if __name__ == "__main__":
    root = tk.Tk()
    root.title("reeds_shepp path")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app = PathViewer(root, paths)
    root.mainloop()
