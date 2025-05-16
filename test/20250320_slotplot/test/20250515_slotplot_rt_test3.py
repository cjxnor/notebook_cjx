import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class AnimationSwitcher:
    def __init__(self, root):
        self.root = root
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # 当前动画对象
        self.ani = None

        # 当前模式
        self.mode = "sin"

        # 按钮切换动画
        btn = tk.Button(root, text="切换动画", command=self.switch_animation)
        btn.pack()

        self.xdata, self.ydata = [], []
        self.line, = self.ax.plot([], [], 'r-')
        self.init_plot()
        self.start_animation("sin")

    def init_plot(self):
        self.ax.set_xlim(0, 2 * np.pi)
        self.ax.set_ylim(-1.5, 1.5)

    def update_sin(self, frame):
        self.xdata.append(frame)
        self.ydata.append(np.sin(frame))
        self.line.set_data(self.xdata, self.ydata)
        return self.line,

    def update_cos(self, frame):
        self.xdata.append(frame)
        self.ydata.append(np.cos(frame))
        self.line.set_data(self.xdata, self.ydata)
        return self.line,

    def start_animation(self, mode):
        self.xdata.clear()
        self.ydata.clear()
        self.line.set_data([], [])

        if self.ani and self.ani.event_source:
            self.ani.event_source.stop()
            self.ani = None

        update_func = self.update_sin if mode == "sin" else self.update_cos
        self.ani = animation.FuncAnimation(
            self.fig,
            update_func,
            frames=np.linspace(0, 2 * np.pi, 128),
            blit=True,
            interval=50,
            repeat=False
        )
        self.canvas.draw()

    def switch_animation(self):
        self.mode = "cos" if self.mode == "sin" else "sin"
        self.start_animation(self.mode)

# 主程序
root = tk.Tk()
root.title("动画切换示例")
app = AnimationSwitcher(root)
root.mainloop()
