import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.spatial import KDTree

# 生成随机障碍物
np.random.seed(42)
obstacles = np.random.rand(10, 2) * 10

# 定制化采样：优先靠近障碍物采样
def customized_sampling(num_points, space_size, obstacles):
    points = np.random.rand(num_points, 2) * space_size
    # 计算每个点到障碍物的距离
    for i in range(len(points)):
        dists = np.linalg.norm(obstacles - points[i], axis=1)
        if np.min(dists) > 2:  # 让采样点更靠近障碍物
            points[i] -= (points[i] - obstacles[np.argmin(dists)]) * 0.3
    return points

# 生成定制化采样点
points = customized_sampling(50, 10, obstacles)

# 构造 PRM
def construct_prm(points, k=5):
    graph = nx.Graph()
    kd_tree = KDTree(points)

    for i, p in enumerate(points):
        graph.add_node(tuple(p))
        _, indices = kd_tree.query(p, k+1)  
        for j in indices[1:]:
            if not check_collision(p, points[j], obstacles):
                graph.add_edge(tuple(p), tuple(points[j]))

    return graph

# 碰撞检测
def check_collision(p1, p2, obstacles):
    for obs in obstacles:
        if np.linalg.norm(np.cross(p2 - p1, p1 - obs)) < 0.3:
            return True
    return False

# 绘制 PRM
def plot_prm(graph, points, obstacles):
    plt.scatter(points[:, 0], points[:, 1], color='blue', label="Samples")
    plt.scatter(obstacles[:, 0], obstacles[:, 1], color='red', label="Obstacles", s=100)
    nx.draw(graph, pos={node: node for node in graph.nodes()}, node_size=30, edge_color='gray')
    plt.legend()
    plt.title("Customized PRM")
    plt.show()

# 测试
graph = construct_prm(points)
plot_prm(graph, points, obstacles)
