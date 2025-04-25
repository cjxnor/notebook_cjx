import math
import sympy as sp
import numpy as np

# 定义变量
phi = sp.Symbol('phi', real=True)

# 常量代入计算
SL = 6          # 车位长度
Er = 0.961      # 后悬
D1 = 0.2        # 安全距离
Al = 2.716      # 轴距
Ef = 0.997      # 前悬

"""
# 1.车辆左转出车位，车辆右前角与车位角点保持安全距离D1，前轮转角需要满足的条件
"""
numerator = (SL - Er - D1)**2 - (Al + Ef)**2
denominator = 2 * Al
rhs = numerator / denominator  # 右边是个常数

# 打印右边数值
rhs_value = float(rhs)
print("右侧常数 =", rhs_value)

# 不等式：cot(phi) ≤ rhs
ineq = sp.cot(phi) <= rhs

# 解不等式（解析形式）
sol = sp.solve(ineq, phi)
print("不等式解：", sol)

# 数值近似（arccot）
phi_lower = float(sp.acot(rhs_value))  # acot(x) = arccot(x)
print("phi ≥", phi_lower, "（弧度）")

# 转角度
phi_deg = np.degrees(phi_lower)
print("phi ≥", phi_deg, "°")

"""
# 2.假如车辆已最大前轮转角出车位，能满足车辆右前角点与车位角点保持安全距离，求最小车位长度
"""
phi = 8.0/15
cot_phi = 1 / math.tan(phi)

# 定义一个实数类型的符号变量
SL2 = sp.Symbol('SL2', real=True)
# 不等式右边表达式
rhs = ((SL2 - Er - D1)**2 - (Al + Ef)**2) / (2 * Al)

# 构建不等式：cot(phi) <= rhs
# sp.Rel() 就是 SymPy 里的 “Relation”（关系表达式）
ineq = sp.solve(sp.Rel(cot_phi, rhs, '<='), SL2)

print("SL2 的取值范围：", ineq)


