import math
import sympy as sp
import numpy as np

# 常量代入计算
SL = 6          # 车位长度
Er = 0.961      # 后悬
D1 = 0.2        # 安全距离
Al = 2.716      # 轴距
Ef = 0.997      # 前悬
phi = 8.0/15
cot_phi = 1 / math.tan(phi)

"""
# 1.假设车辆与车位角度差为theta，摆正车辆（车辆与车位角度差为0°），需要向前走多远
"""
T3N = 0.5
sin_theta2 = T3N / (Al*cot_phi)

theta2_rad_1 = math.asin(sin_theta2)
theta2_degree_1 = math.degrees(theta2_rad_1)
print("theta2 的值：", theta2_degree_1)

