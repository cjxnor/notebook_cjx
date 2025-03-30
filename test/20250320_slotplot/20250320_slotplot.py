# -*- coding: utf-8 -*-
import json
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
# from adjustText import adjust_text
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# 用字典存储相同坐标的数量
from collections import defaultdict
# import pyautogui
# from PIL import ImageGrab
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
    global canvas  # 让 canvas 变量可全局更新

    # 清除旧的图形
    for widget in canvas_frame.winfo_children():
        widget.destroy()

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

    global label
    label.config(text="")
    label.config(text=f"pdc_psolt_id: {pdc_psolt_id}\npcd_psolt_latreftype: {pcd_psolt_latreftype}\npcd_psolt_slottype: {pcd_psolt_slottype}\nPDC_PSolt_attribute_Status: {PDC_PSolt_attribute_Status}")
    # label.pack(side="left", padx=10, pady=10)

    # # 绘图
    global fig
    fig, ax = plt.subplots()
    # ax.scatter(x_coords, y_coords, color="blue", label=f"Timestamp: {selected_timestamp}")
    ax.scatter(x_coords, y_coords, color="blue")
    ax.scatter(0.0, 0.0, color="red", s=100)

    point_counts = defaultdict(int)
    # 在每个点旁边添加标签
    offset_buf = 0.6
    for i, (x, y, index, point_status) in enumerate(zip(x_coords, y_coords, indexs, points_status)):
        offset = point_counts[(x, y)] * offset_buf  # 每个相同坐标的点向上偏移 0.1
        text = ax.text(x, y + offset, f"{index}: {point_status}\n({x:.2f}, {y:.2f})", fontsize=10, ha="right", va="bottom", color="red")
        # texts.append(text)
        point_counts[(x, y)] += 1  # 记录这个坐标已经用了几次

    # 自动调整标签，避免重叠
    # adjust_text(texts, arrowprops=dict(arrowstyle="->", color='gray', lw=0.5))

    # 固定 x, y 轴范围
    # plt.xlim(-10, 10)  # x 轴范围固定为 0 到 6
    # plt.ylim(-10, 10)  # y 轴范围固定为 0 到 60
    axis_buff = 2.0
    plt.xlim(min(min(x_coords) - axis_buff, -axis_buff), max(max(x_coords) + axis_buff, axis_buff))
    plt.ylim(min(min(y_coords) - axis_buff, -axis_buff), max(max(y_coords) + axis_buff, axis_buff))

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(f"points - {selected_timestamp}")
    # ax.legend()
    ax.grid(True)
    # ax.show()

    # 将 Matplotlib 图形嵌入到 Tkinter 中
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)  # 将 Matplotlib 图形传入 Tkinter 根窗口
    canvas.draw()  # 绘制图形
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # 将图形添加到窗口

    plt.close(fig)

# 📌 处理下拉菜单选择事件
def on_timestamp_selected(event):
    selected_timestamp = timestamp_var.get()
    plot_coordinates(selected_timestamp)

# 监听窗口关闭事件
def on_closing():
    root.quit()  # 停止 Tkinter 主循环，确保脚本退出
    root.destroy()  # 彻底销毁窗口

# 保存图片的函数
def save_plot():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"),
                                                        ("JPEG files", "*.jpg"),
                                                        ("PDF files", "*.pdf"),
                                                        ("SVG files", "*.svg")])
    # if file_path:
    #     # 获取窗口位置
    #     x = root.winfo_rootx()
    #     y = root.winfo_rooty()
    #     w = root.winfo_width()
    #     h = root.winfo_height()

    #     # 截图并保存
    #     screenshot = pyautogui.screenshot(region=(x, y, w, h))
    #     screenshot.save(file_path)
    #     print(f"Saved screenshot: {file_path}")

    if file_path:
        fig.savefig(file_path, dpi=300, bbox_inches="tight")
        print(f"Saved: {file_path}")

def open_json_file():
    """打开 JSON 文件并显示内容"""
    global file_path
    # 获取当前路径并指定 data 目录
    current_dir = os.getcwd()  # 获取当前工作目录
    data_dir = os.path.join(current_dir, 'data')  # 拼接成 data 目录路径
    file_path = filedialog.askopenfilename(
        title="选择 JSON 文件",
        initialdir=data_dir,  # 设置初始显示路径为当前路径下的 data 目录
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
    )

    if file_path:
        global json_data
        json_data = read_json_lines(file_path)
        timestamps = get_timestamps(json_data)
        global sorted_timestamps
        sorted_timestamps = sorted(timestamps)
        global dropdown
        # global timestamp_var
        dropdown["values"] = sorted_timestamps
        # timestamp_var.set(sorted_timestamps)
        # dropdown.pack(pady=10)
        # "<<"ComboboxSelected">>"：这是一个专门用于 Combobox 控件的事件，表示用户从下拉菜单中选择了一项。
        dropdown.bind("<<ComboboxSelected>>", on_timestamp_selected)
        # print(file_path)
        dropdown.current(0)  # 默认选中第一个
        plot_coordinates(sorted_timestamps[0])

def cycle_options():
    global dropdown
    current_index = sorted_timestamps.index(dropdown.get())
    next_index = (current_index + 1) % len(sorted_timestamps)
    dropdown.set(sorted_timestamps[next_index])
    on_timestamp_selected(None)

# 📌 读取 JSON 文件
# file_path = "20250321_pdc_slot.json"  # 请替换为你的 JSON 文件路径
# json_data = read_json_lines(file_path)
# timestamps = get_timestamps(json_data)

# 📌 创建 Tkinter 窗口
root = tk.Tk()
root.title("draw slot")
root.geometry("1000x800")  # 设置窗口大小（宽 x 高）
root.resizable(True, True)  # 允许水平和垂直方向调整窗口大小
# 用来为 窗口关闭事件 定义一个 回调函数，
# "WM_DELETE_WINDOW": 这是一个特殊的协议，表示用户点击窗口的 关闭按钮 时触发的事件。
root.protocol("WM_DELETE_WINDOW", on_closing)

# Tkinter 中的一种 变量类 的实例化方法，StringVar 用来表示和管理一个字符串类型的变量。
# 这个变量可以与 Tkinter 界面上的组件（如 Label、Entry 等）绑定，从而实现动态更新界面元素的值。
timestamp_var = tk.StringVar()
# 排序选项列表
# sorted_timestamps = sorted(timestamps)
dropdown = ttk.Combobox(root, textvariable=timestamp_var)
dropdown.pack(pady=10)
# dropdown.bind("<<ComboboxSelected>>", on_timestamp_selected)

# 创建按钮并绑定到循环选项的函数
button = tk.Button(root, text="Next", command=cycle_options)
button.pack()

# 显示绘图的框架
canvas_frame = tk.Frame(root)
canvas_frame.pack(fill=tk.BOTH, expand=True)

# 添加说明性文本
pdc_psolt_id = ""
pcd_psolt_latreftype = ""
pcd_psolt_slottype = ""
PDC_PSolt_attribute_Status = ""
label = tk.Label(root, text=f"pdc_psolt_id: {pdc_psolt_id}\npcd_psolt_latreftype: {pcd_psolt_latreftype}\npcd_psolt_slottype: {pcd_psolt_slottype}\nPDC_PSolt_attribute_Status: {PDC_PSolt_attribute_Status}",
                 font=("Arial", 12), justify="left", anchor="w")
label.pack(side="left", padx=10, pady=10)   # 将标签放入窗口并显示

# 创建菜单栏
menu_bar = tk.Menu(root)
# 创建“文件”菜单
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="打开 JSON 文件", command=open_json_file)
# file_menu.add_command(label="保存 JSON 文件", command=save_json_file)
file_menu.add_separator()
# file_menu.add_command(label="退出", command=root.quit)
# menu_bar.add_cascade(label="文件", menu=file_menu)
file_menu.add_command(label="保存图片", command=save_plot)
file_menu.add_separator()
file_menu.add_command(label="退出", command=root.quit)

# 添加“文件”菜单到菜单栏
menu_bar.add_cascade(label="文件", menu=file_menu)

# 将菜单栏添加到 Tkinter 窗口
root.config(menu=menu_bar)

# 运行 Tkinter 界面
root.mainloop()
