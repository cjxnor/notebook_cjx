# -*- coding: utf-8 -*-
# 在20250422_reeds_shepp_hmi2.py的基础上调用CurvesGenerator.reeds_shepp_test测试reeds_shepp曲线
# python 3.12.7

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
                "/../../../../MotionPlanning/")

import CurvesGenerator.reeds_shepp_test as rs

MAX_STEER = 8.0/15  # [rad] maximum steering angle
WB = 2.716  # [m] Wheel base
MOVE_STEP = 0.4  # [m] path interporate resolution

# 起点与终点 (x, y, yaw in rad)
# start = (2.0, 2.0, np.deg2rad(0))
start = None
# goal = (2.0, 2.5, np.deg2rad(0))
goal = None

maxc = math.tan(MAX_STEER) / WB     # 最大曲率

paths = []
# rs.calc_all_paths(start[0], start[1], start[2], goal[0], goal[1], goal[2], 
#                           maxc, step_size=MOVE_STEP) # MOVE_STEP = 0.4

class PathViewer:
    def __init__(self, master):
        self.master = master
        self.paths = paths
        self.index = 0

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # ctypes
        # self.label_ctypes = tk.Label(master, text="", font=("Arial", 14))
        # self.label_ctypes.pack()

        # 起点变量（默认 0）
        self.start_x = tk.StringVar(value='0')
        self.start_y = tk.StringVar(value='0')
        self.start_theta = tk.StringVar(value='0')
        # 终点变量（默认 0）
        self.end_x = tk.StringVar(value='0')
        self.end_y = tk.StringVar(value='0')
        self.end_theta = tk.StringVar(value='0')

        # 输入框区域
        frame = tk.Frame(self.master)
        frame.pack(pady=10)
        # tk.Label(frame, text="Start (x,y,θ):").grid(row=0, column=0)
        # self.start_entry = tk.Entry(frame, width=20)
        # self.start_entry.grid(row=0, column=1)

        # 起点输入框
        tk.Label(frame, text="Start x:").grid(row=0, column=0)
        tk.Entry(frame, textvariable=self.start_x, width=6).grid(row=0, column=1)
        tk.Label(frame, text="y:").grid(row=0, column=2)
        tk.Entry(frame, textvariable=self.start_y, width=6).grid(row=0, column=3)
        tk.Label(frame, text="θ/°:").grid(row=0, column=4)
        tk.Entry(frame, textvariable=self.start_theta, width=6).grid(row=0, column=5)
        # 终点输入框
        tk.Label(frame, text="End   x:").grid(row=1, column=0)
        tk.Entry(frame, textvariable=self.end_x, width=6).grid(row=1, column=1)
        tk.Label(frame, text="y:").grid(row=1, column=2)
        tk.Entry(frame, textvariable=self.end_y, width=6).grid(row=1, column=3)
        tk.Label(frame, text="θ/°:").grid(row=1, column=4)
        tk.Entry(frame, textvariable=self.end_theta, width=6).grid(row=1, column=5)

        # 所有输入框绑定自动更新
        for var in [self.start_x, self.start_y, self.start_theta,
                    self.end_x, self.end_y, self.end_theta]:
            var.trace_add("write", self.update_plot)

        self.update_plot()

        # tk.Label(frame, text="Goal (x,y,θ):").grid(row=2, column=0)
        # self.end_entry = tk.Entry(frame, width=20)
        # self.end_entry.grid(row=2, column=1)

        draw_button = tk.Button(frame, text="Calc RS", command=self.calc_rs)
        draw_button.grid(row=2, column=0)     # , columnspan=2, pady=5

        # 总长
        # self.label_L = tk.Label(master, text="", font=("Arial", 14))
        # self.label_L.pack()

        self.info_text = tk.Text(frame, height=6, width=60, font=("Courier", 10))
        # self.info_text.pack()
        self.info_text.grid(row=3, column=0, columnspan=10, padx=5, pady=5)
        # 配置左对齐标签
        self.info_text.tag_configure("left", justify="left")

        # self.index = (self.index + 1) % len(self.paths)  # 循环切换
        self.prev_button = tk.Button(frame, text="Prev", command=lambda:self.plot_next_path(-1))
        self.prev_button.grid(row=4, column=0, padx=5, pady=5)
        self.next_button = tk.Button(frame, text="Next", command=lambda:self.plot_next_path(1))
        self.next_button.grid(row=4, column=1, padx=5, pady=5)
        # self.button.pack()

        # self.max_x = max(x for path in paths for x in path.x)
        # self.min_x = min(x for path in paths for x in path.x)
        # self.max_y = max(y for path in paths for y in path.y)
        # self.min_y = min(y for path in paths for y in path.y)

        # self.plot_next_path()  # 初始显示第一条路径

    def plot_next_path(self, flag):
        self.ax.clear()
        if not self.paths:
            return
        
        if flag > 0:
            self.index = (self.index + 1) % len(self.paths)  # 向后循环切换
        elif flag < 0:
            self.index = (self.index - 1) % len(self.paths)  # 向前循环切换

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

        axis_buff = 5
        max_x = max_x + axis_buff
        min_x = min_x - axis_buff
        max_y = max_y + axis_buff
        min_y = min_y - axis_buff

        self.ax.set_xlim(min_x, max_x)
        self.ax.set_ylim(min_y, max_y)

        delx = abs(max_x - min_x)
        dely = abs(max_y - min_y)

        al = 0.05 * delx  # 箭头线段长
        hw = 0.5 * al   # 箭头宽度
        hl = al         # 箭头长度

        dx = np.cos(start[2]) * al  # 箭头长度 * 方向
        dy = np.sin(start[2]) * al
        # hw = 0.05 * (max_y - min_y)
        # hl = 1.5 * hw
        self.ax.arrow(start[0], start[1], dx, dy, head_width=hw, head_length=hl, 
                      fc='green', ec='green')

        dx = np.cos(goal[2]) * al  # 箭头长度 * 方向
        dy = np.sin(goal[2]) * al
        self.ax.arrow(goal[0], goal[1], dx, dy, head_width=hw, head_length=hl, 
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

        # self.index = (self.index + 1) % len(self.paths)  # 循环切换

    def calc_rs(self):
        self.ax.clear()
        # self.ax.set_xlim(0, 100)
        # self.ax.set_ylim(0, 100)
        # self.ax.set_title("起点和终点示意图")

        try:
            # sx, sy, stheta = map(float, self.start_entry.get().strip().split(','))
            # ex, ey, etheta = map(float, self.end_entry.get().strip().split(','))
            sx = float(self.start_x.get())
            sy = float(self.start_y.get())
            st = float(self.start_theta.get())
            ex = float(self.end_x.get())
            ey = float(self.end_y.get())
            et = float(self.end_theta.get())

            # print("起点输入内容：", self.start_entry.get())
            # print("终点输入内容：", self.end_entry.get())
            # print(f"sx:{sx}, sy:{sy}, stheta:{stheta}")
            # print(f"ex:{ex}, ey:{ey}, etheta:{etheta}")
            global start, goal
            start = [sx, sy, np.deg2rad(st)]
            goal = [ex, ey, np.deg2rad(et)]

            global paths
            paths = rs.calc_all_paths(start[0], start[1], start[2], goal[0], goal[1], goal[2], 
                          maxc, step_size=MOVE_STEP) # MOVE_STEP = 0.4
            
            self.paths = paths
            self.index = 0
            self.plot_next_path(0)  # 初始显示第一条路径
        except:
            print("输入格式错误！请使用 x,y,theta 的格式")

    def update_plot(self, *args):
        try:
            # 起点数据
            sx = float(self.start_x.get())
            sy = float(self.start_y.get())
            st = float(self.start_theta.get())

            # 终点数据
            ex = float(self.end_x.get())
            ey = float(self.end_y.get())
            et = float(self.end_theta.get())
        except ValueError:
            return  # 输入不合法，跳过

        self.ax.clear()
        self.paths.clear()
        # self.ax.set_xlim(0, 100)
        # self.ax.set_ylim(0, 100)
        # self.ax.set_title("起点示意图")        

        axis_buff = 5
        x_min = min(-10, sx - axis_buff, ex - axis_buff)
        x_max = max(10, sx + axis_buff, ex + axis_buff)
        y_min = min(-10, sy - axis_buff, ey - axis_buff)
        y_max = max(10, sy + axis_buff, ey + axis_buff)

        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)

        dx = abs(x_max - x_min)
        dy = abs(y_max - y_min)

        al = 0.05 * dx  # 箭头线段长
        hw = 0.5 * al   # 箭头宽度
        hl = al         # 箭头长度
        # print(f"al={al}, hw={hw}, hl={hl}")

        # 起点：绿色点 + 朝向箭头
        self.ax.plot(sx, sy, 'go', label="Start")
        self.ax.annotate(f"Start\nθ={st}", (sx, sy), textcoords="offset points", xytext=(0, 10), ha='center')
        # head_width=2,箭头头部宽度     head_length=2,箭头头部长度
        self.ax.arrow(sx, sy, al * np.cos(np.deg2rad(st)), al * np.sin(np.deg2rad(st)), 
                      head_width=hw, head_length=hl, fc='green', ec='green')

        # 终点：红色点 + 朝向箭头
        self.ax.plot(ex, ey, 'ro', label="End")
        self.ax.annotate(f"End\nθ={et}", (ex, ey), textcoords="offset points", xytext=(0, 10), ha='center')
        self.ax.arrow(ex, ey, al * np.cos(np.deg2rad(et)), al * np.sin(np.deg2rad(et)), 
                      head_width=hw, head_length=hl, fc='red', ec='red')

        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

# 监听窗口关闭事件
def on_closing():
    root.quit()  # 停止 Tkinter 主循环，确保脚本退出
    root.destroy()  # 彻底销毁窗口

if __name__ == "__main__":
    root = tk.Tk()
    root.title("reeds_shepp path")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app = PathViewer(root)
    root.mainloop()
