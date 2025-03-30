import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# 生成带噪声的轨迹数据
x = np.linspace(0, 10, 100)
y = np.sin(x) + np.random.normal(0, 0.2, len(x))  # 添加噪声

# 使用 Savitzky-Golay 滤波器平滑数据
y_smooth = savgol_filter(y, window_length=11, polyorder=3)  # 窗口大小 11，多项式阶数 3

# 画图
plt.plot(x, y, label="Noisy Data", linestyle="dashed", alpha=0.5)
plt.plot(x, y_smooth, label="Smoothed Data", color='red')
plt.legend()
plt.title("Savitzky-Golay Smoothing")
plt.show()
