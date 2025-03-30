import matplotlib.pyplot as plt

# 数据
x = [1, 2, 3, 4, 5]
y = [5, 4, 3, 2, 1]

# 创建散点图
plt.scatter(x, y)

# 添加标题和标签
plt.title('Scatter Plot Example')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')

# 显示图形
plt.show()
