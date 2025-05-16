# -*- coding: utf-8 -*-
# 绘制动图
import json
import matplotlib.pyplot as plt
# 用字典存储相同坐标的数量
from collections import defaultdict
import os

fig = None
json_data = []
sorted_timestamps = []
# 📌 读取 JSON Lines 文件
def read_json_lines(file_path):
    data = []
    with open(file_path, "r") as file:
        for line in file:
            try:
                json_obj = json.loads(line.strip())  # 解析每行 JSON
                data.append(json_obj)
            except json.JSONDecodeError:
                print(f"⚠️ 无法解析行: {line}")
    return data

# 📌 获取所有 timestamp
def get_timestamps(data):
    return list({entry["timestamp"] for entry in data})  # 去重

# 📌 绘制坐标点
def plot_coordinates(selected_timestamp):
    # global canvas  # 让 canvas 变量可全局更新

    # 过滤出选中的 timestamp 对应的坐标点
    filtered_data = [entry for entry in json_data if entry["timestamp"] == selected_timestamp]
    
    if not filtered_data:
        print(f"⚠️ 没有找到 timestamp: {selected_timestamp}")
        return
    
    # print(filtered_data[0]["obj1start_pos"]["x"])
    # # 提取坐标点
    indexs = ["obj1start_pos", "obj1end_pos", "slotobjstartpt_pos", "slotobjendpt_pos", "obj2start_pos", "obj2end_pos", ]
    x_coords = [filtered_data[0][i]["x"] for i in indexs]
    y_coords = [filtered_data[0][i]["y"] for i in indexs]
    points_status = [filtered_data[0][i]["point_status"] for i in indexs]

    # slot属性
    global pdc_psolt_id
    pdc_psolt_id = filtered_data[0]["pdc_psolt_id"]
    global pcd_psolt_latreftype
    pcd_psolt_latreftype = filtered_data[0]["pcd_psolt_latreftype"]
    global pcd_psolt_slottype
    pcd_psolt_slottype = filtered_data[0]["pcd_psolt_slottype"]
    global PDC_PSolt_attribute_Status
    PDC_PSolt_attribute_Status = filtered_data[0]["PDC_PSolt_attribute_Status"]

    plt.scatter(x_coords, y_coords, color="blue")
    plt.scatter(0.0, 0.0, color="red", s=100)

    point_counts = defaultdict(int)
    # 在每个点旁边添加标签
    offset_buf = 0.6
    for i, (x, y, index, point_status) in enumerate(zip(x_coords, y_coords, indexs, points_status)):
        offset = point_counts[(x, y)] * offset_buf  # 每个相同坐标的点向上偏移 0.1
        text = plt.text(x, y + offset, f"{index}: {point_status}\n({x:.2f}, {y:.2f})", fontsize=10, ha="right", va="bottom", color="red")
        # texts.append(text)
        point_counts[(x, y)] += 1  # 记录这个坐标已经用了几次

    # 固定 x, y 轴范围
    # plt.xlim(-10, 10)  # x 轴范围固定为 0 到 6
    # plt.ylim(-10, 10)  # y 轴范围固定为 0 到 60
    axis_buff = 2.0
    plt.xlim(min(min(x_coords) - axis_buff, -axis_buff), max(max(x_coords) + axis_buff, axis_buff))
    plt.ylim(min(min(y_coords) - axis_buff, -axis_buff), max(max(y_coords) + axis_buff, axis_buff))
    plt.axis('equal')  # 设置缩放比例一致

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"points - {selected_timestamp}")
    # ax.legend()
    plt.grid(True)
    # ax.show()

    plt.pause(0.005)


# 📌 读取 JSON 文件
current_dir = os.getcwd()  # 获取当前工作目录
print(f"pwd : {current_dir}")
file_path = os.path.join(current_dir, 'test/20250320_slotplot/data/20250418_pdc_slot_rt.json')  # 拼接成 data 目录路径
json_data = read_json_lines(file_path)
timestamps = get_timestamps(json_data)
# global sorted_timestamps
sorted_timestamps = sorted(timestamps)

plt.ion()
for k in range(len(sorted_timestamps)):
    plt.cla()
    # manager = plt.get_current_fig_manager()
    # manager.window.move(100, 200)  # 将窗口移动到屏幕 (100, 200)
    plot_coordinates(sorted_timestamps[k])
plt.ioff()
plt.show()

