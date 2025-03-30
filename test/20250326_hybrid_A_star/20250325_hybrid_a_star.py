import numpy as np
import heapq
import matplotlib.pyplot as plt
# import rsplan
from mpl_toolkits.mplot3d import Axes3D

# 车辆参数
MAX_STEER = np.radians(35)  # 最大转向角（弧度）
STEP_SIZE = 1.0  # 运动步长
WB = 2.5  # 轴距

# 地图设置（0 表示可行驶区域，1 表示障碍物）
GRID_SIZE = 20
# (10, 10),, (13, 12), (14, 12), (15, 12), (16, 12), (17, 12)
OBSTACLES = [(10, 11), (10, 12), (11, 12), (12, 12)]

open_list = []
# set()不允许重复元素
closed_set = set()

class Node:
    """ A* 结点 """
    def __init__(self, x, y, theta, cost, parent):
        self.x = x
        self.y = y
        self.theta = theta  # 方向角
        self.cost = cost  # g(n)
        self.parent = parent  # 上一个节点

    # 如果一个类定义了__lt__，那么该类的对象可以使用 < 进行比较
    def __lt__(self, other):
        return self.cost < other.cost  # 堆排序依据

def heuristic(node, goal):
    """ 使用 Dubins 轨迹计算启发式 """
    # qs = (node.x, node.y, node.theta)
    # qe = (goal.x, goal.y, goal.theta)
    # path = rsplan.ReedsShepp(qs, qe, 5.5)
    delx = goal.x - node.x
    dely = goal.y - node.x
    return abs(delx) + abs(dely)

def is_valid(x, y):
    """ 检查是否在地图范围内且没有碰撞 """
    if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
        return False
    if (int(x), int(y)) in OBSTACLES:
        return False
    return True

def motion_model():
    """ 车辆运动模型，返回可扩展的 5 个方向 """
    return [
        (STEP_SIZE, MAX_STEER),
        (STEP_SIZE, -MAX_STEER),
        (STEP_SIZE, 0),
        (STEP_SIZE, MAX_STEER / 2),
        (STEP_SIZE, -MAX_STEER / 2)
    ]

def hybrid_a_star(start, goal):
    """ 混合 A* 算法 """
    
    # 堆的排序规则基于元组的第一个元素（即第一个值作为优先级）。
    # 如果第一个值相同，则根据第二个值的字母顺序（字符串比较）进行排序
    heapq.heappush(open_list, (0, start))  # (f(n), Node)
    
    # global open_list
    while open_list:
        _, current = heapq.heappop(open_list)

        global closed_set
        # 到达目标
        if np.hypot(current.x - goal.x, current.y - goal.y) < STEP_SIZE:
            print(len(closed_set))
            print(len(open_list))
            return current

        # 元组作为set()的元素
        closed_set.add((current.x, current.y, current.theta))

        # 扩展子节点
        for motion in motion_model():   # step_size, steer
            new_x = current.x + motion[0] * np.cos(current.theta)
            new_y = current.y + motion[0] * np.sin(current.theta)
            new_theta = current.theta + motion[0] / WB * np.tan(motion[1])

            if not is_valid(new_x, new_y):
                continue

            new_node = Node(new_x, new_y, new_theta, current.cost + STEP_SIZE, current)
            # plt.scatter(new_x, new_x, color="black")
            
            if (new_x, new_y, new_theta) in closed_set:
                continue

            f_cost = new_node.cost + heuristic(new_node, goal)
            heapq.heappush(open_list, (f_cost, new_node))

    return None

def extract_path(node):
    """ 回溯路径 """
    path_x, path_y = [], []
    while node:
        path_x.append(node.x)
        path_y.append(node.y)
        node = node.parent
    return path_x[::-1], path_y[::-1]

def plot_grid():
    """ 绘制网格地图和障碍物 """
    plt.figure(figsize=(8, 8))
    # ax = fig.add_subplot(111, projection='3d')

    # global closed_set
    # 画三维图太费时
    # for x, y, theta in closed_set:
    #     ax.scatter(x, y, theta, color='b', s=50)  # 绘制点
    #     # 计算箭头方向 (这里假设 z 轴为 θ)
    #     dx = np.cos(theta) * 0.5  # 控制箭头长度
    #     dy = np.sin(theta) * 0.5
    #     dz = 0
    #     ax.quiver(x, y, theta, dx, dy, dz, color='r', arrow_length_ratio=0.2)  # 绘制方向箭头

    # for x, y, theta in closed_set:
    #     plt.scatter(x, y, color="red")

    # global open_list
    # n = int(len(open_list) * 0.9)  # 计算前 20% 的索引
    # for cost, node in open_list:
    #     plt.scatter(node.x, node.y, color="red")

    plt.xlim(0, GRID_SIZE)
    plt.ylim(0, GRID_SIZE)
    plt.grid(True)

    for (ox, oy) in OBSTACLES:
        plt.scatter(ox, oy, color="black", s=100)

def plot_path(path_x, path_y):
    """ 绘制最终路径 """
    plt.plot(path_x, path_y, "-r", linewidth=2, label="Hybrid A* Path")
    plt.legend()
    plt.show()

# 设定起点和终点 np.radians(0)：将角度 0° 转换为弧度
start = Node(2, 2, np.radians(0), 0, None)
# goal = Node(18, 18, np.radians(0), 0, None)
goal = Node(8, 8, np.radians(0), 0, None)


# 运行混合 A*
result = hybrid_a_star(start, goal)

if result:
    path_x, path_y = extract_path(result)
    plot_grid()
    plot_path(path_x, path_y)
else:
    print("未找到路径")
