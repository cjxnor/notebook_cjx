import numpy as np
import matplotlib.pyplot as plt

def generate_vehicle_hexagon(length, width, delta):
    """
    生成标准六边形车辆模型顶点（局部坐标系，朝向x轴）。
    length: 车辆总长
    width: 车辆宽度
    delta: 前后削角长度
    返回：6个顶点的坐标，按顺时针排列（numpy array: shape (6, 2)）
    """
    half_w = width / 2
    front = length / 2
    back = -length / 2

    vertices = np.array([
        [back + delta, -half_w],
        [front - delta, -half_w],
        [front, 0],
        [front - delta, half_w],
        [back + delta, half_w],
        [back, 0],
    ])
    return vertices


def transform_polygon(polygon, x, y, theta):
    """
    对多边形顶点进行仿射变换
    polygon: (N, 2) array, 原始局部坐标顶点
    x, y: 平移坐标
    theta: 旋转角度（单位：弧度）
    """
    rot = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])
    # @ 是矩阵乘法运算符，由于polygon是6*2矩阵，6个(x,y)是行向量堆叠起来的
    # 坐标转换倾向于使用(x,y)的列向量进行，所以会将polygon进行转置再与旋转矩阵相乘
    transformed = (rot @ polygon.T).T + np.array([x, y])
    return transformed


def get_axes(polygon):
    # 获取两个多边形的所有边的法向量（单位向量）
    axes = []
    n = len(polygon)
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        edge = p2 - p1
        # (x,y)绕原点逆时针旋转90度->(-y,x)     顺时针旋转90度->(y,-x)
        normal = np.array([-edge[1], edge[0]])  # 90度旋转
        # 进行归一化，得到单位向量
        normal = normal / np.linalg.norm(normal)
        axes.append(normal)
    return axes


def is_collision(poly1, poly2):
    """
    判断两个凸多边形是否碰撞，基于 Separating Axis Theorem (SAT)
    poly1, poly2: (N, 2) array，按顺时针排列的顶点坐标
    """
    # 计算polygon所有点在axis上的投影，并返回投影的最小/最大值
    def project(polygon, axis):
        dots = polygon @ axis
        return [dots.min(), dots.max()]

    axes = get_axes(poly1) + get_axes(poly2)

    for axis in axes:
        proj1 = project(poly1, axis)
        proj2 = project(poly2, axis)
        if proj1[1] < proj2[0] or proj2[1] < proj1[0]:
            return False  # 分离轴存在
    return True  # 所有轴都重叠 => 碰撞


def draw_projection(polygon, axis, color, label):
    dots = polygon @ axis
    min_proj = dots.min()
    max_proj = dots.max()
    plt.plot([min_proj, max_proj], [0, 0], lw=5, color=color, label=label)

def visualize_sat(poly1, poly2):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Draw original polygons
    poly1_closed = np.vstack([poly1, poly1[0]])
    poly2_closed = np.vstack([poly2, poly2[0]])
    ax.plot(poly1_closed[:, 0], poly1_closed[:, 1], 'b-', label="Poly1")
    ax.plot(poly2_closed[:, 0], poly2_closed[:, 1], 'r-', label="Poly2")
    ax.set_aspect('equal')
    ax.grid(True)
    
    # Pick one axis for demonstration
    axis = get_axes(poly1)[0]
    
    # Draw the axis as an arrow
    center = np.mean(poly1, axis=0)
    ax.quiver(center[0], center[1], axis[0], axis[1], angles='xy', scale_units='xy',
              scale=1, color='green', width=0.01, label='Projection Axis')

    # Do the projection onto the axis and show on a side plot
    plt.figure(figsize=(8, 2))
    draw_projection(poly1, axis, 'blue', 'Poly1 projection')
    draw_projection(poly2, axis, 'red', 'Poly2 projection')
    plt.title('Projection onto Axis')
    plt.yticks([])
    plt.legend()
    plt.grid(True)
    plt.xlabel('Projection Value')
    plt.tight_layout()
    plt.show()

# 参数设定
length, width, delta = 4.5, 2.0, 0.5
veh_poly = generate_vehicle_hexagon(length, width, delta)
veh_pose = (10.0, 5.0, np.pi/6)  # 位置 (x, y)，朝向 θ

# 变换后的车辆六边形
veh_world = transform_polygon(veh_poly, *veh_pose)

# 假设障碍物是一个矩形
obstacle = np.array([[9, 4], [11, 4], [11, 6], [9, 6]])

# 检测碰撞
if is_collision(veh_world, obstacle):
    print("碰撞！")
else:
    print("安全~")

# Example convex polygons (could represent rotated rectangles or hex shapes)
poly1 = np.array([[0, 0], [2, 0], [2, 1], [0, 1]])        # Box at origin
poly2 = np.array([[1.5, 0.5], [3.5, 0.5], [3.5, 1.5], [1.5, 1.5]])  # Overlapping

visualize_sat(poly1, poly2)