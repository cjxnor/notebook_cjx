import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Bézier曲线计算
def bernstein(n, i, t):
    """计算Bernstein基函数"""
    from math import comb  # Python 3.8+ 支持 comb
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

def bezier_curve(control_points, num_points=100):
    """计算 Bézier 曲线点"""
    n = len(control_points) - 1  # 阶数
    t_values = np.linspace(0, 1, num_points)
    curve = np.zeros((num_points, 2))
    
    for i in range(n + 1):
        curve += np.outer(bernstein(n, i, t_values), control_points[i])
    
    return curve

# 交互式绘图
class BezierInteractive:
    def __init__(self, control_points):
        self.control_points = np.array(control_points)
        self.fig, self.ax = plt.subplots()
        self.cid = None  # 记录拖动事件ID
        self.selected_idx = None  # 选中的点索引
        
        # 绘制初始曲线
        self.update_plot()
        
        # 绑定鼠标事件
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.fig.canvas.mpl_connect("button_release_event", self.on_release)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)
    
    def update_plot(self):
        """更新曲线和控制点"""
        self.ax.clear()
        curve = bezier_curve(self.control_points)
        
        # 画 Bézier 曲线
        self.ax.plot(curve[:, 0], curve[:, 1], 'b-', label="5阶 Bézier 曲线")
        
        # 画控制点和控制线
        self.ax.plot(self.control_points[:, 0], self.control_points[:, 1], 'ro-', label="控制点")
        
        # 设置图例 & 坐标轴
        self.ax.legend()
        self.ax.set_title("可拖拽的 5 阶 Bézier 曲线")
        self.ax.set_xlim(-1, 6)
        self.ax.set_ylim(-1, 6)
        self.fig.canvas.draw()
    
    def on_click(self, event):
        """检测鼠标点击控制点"""
        if event.inaxes != self.ax:
            return
        for i, (x, y) in enumerate(self.control_points):
            if np.hypot(x - event.xdata, y - event.ydata) < 0.2:
                self.selected_idx = i
                break
    
    def on_release(self, event):
        """释放鼠标"""
        self.selected_idx = None
    
    def on_motion(self, event):
        """拖动控制点"""
        if self.selected_idx is None or event.inaxes != self.ax:
            return
        self.control_points[self.selected_idx] = [event.xdata, event.ydata]
        self.update_plot()

# 初始控制点（6 个点）
control_points = [[0, 0], [1, 3], [2, 4], [3, 2], [4, 3], [5, 0]]

# 运行交互式 Bézier 曲线
BezierInteractive(control_points)
plt.show()
