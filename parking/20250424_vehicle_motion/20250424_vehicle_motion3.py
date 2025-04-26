# -*- coding: utf-8 -*-
# 在20250424_vehicle_motion2.py的基础上实现左侧水平车位泊出
import math
import numpy as np
import tkinter as tk
from functools import partial
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

# 参数设置
# radius = 10            # 圆的半径
# eks2
RF = 3.713  # [m] distance from rear to vehicle front end of vehicle  后轴中心到车头的距离
RB = 0.961  # [m] distance from rear to vehicle back end of vehicle   后轴中心到车尾的距离
W_2 = 0.965  # [m] half width of vehicle
WD = 0.7 * W_2 * 2  # [m] distance between left-right wheels
WB = 2.716  # [m] Wheel base
TR = 0.35  # [m] Tyre radius
TW = 0.3  # [m] Tyre width
MAX_STEER = 8.0/15  # [rad] maximum steering angle

# car_length = RF + RB      # 车辆长度
# car_width = W       # 车辆宽度
omega = 0.5           # 角速度
center = (0, 0)       # 圆心
fps = 30
total_time = 10       # 动画时长（秒）

vehicle_pose = []
# 车辆角点坐标
corners = []
# t = frame / fps
# angle = omega * t % (2 * np.pi)
# center_x = center[0] + radius * np.cos(angle)
# center_y = center[1] + radius * np.sin(angle)
# theta = (angle + np.pi / 2) % (2 * np.pi)  # 切线方向
t = 10
fps = 30
center_x = 0
center_y = 0
# 后轴中心最小转弯半径
radius = 5.68
# 左转右后轮最小转弯半径
radius_r_wheel = radius + W_2
# 左转右后角点最小转弯半径
radius_rr = math.sqrt(radius_r_wheel**2 + RB**2)
# 左转右前角点最小转弯半径
radius_fr = math.sqrt(radius_r_wheel**2 + RF**2)
print(f"r_rw = {radius_r_wheel}, r_rr = {radius_rr}, r_fr = {radius_fr}")

# 1.圆形路径
for i in range(t * fps + 1):
    angle = i * (2 * np.pi / (t * fps))
    vehicle_x = center_x + radius * np.cos(angle)
    vehicle_y = center_y + radius * np.sin(angle)
    vehicle_theta = (angle + np.pi / 2) % (2 * np.pi)  # 切线方向
    # vehicle_pose.append([vehicle_x, vehicle_y, vehicle_theta])

# 2.挪库路径 前进0.5m，后退1.0m
"""
s_f = 0.5   # 前进长度
s_r = 1.0   # 后退长度
s_theta_f = s_f / radius
s_theta_r = s_r / radius
# for i in range(0, 1):
# // 是除法只保留整数部分
start = 0                       # (t * fps + 1) // 3
end = (t * fps + 1) // 3        # (i + 1) * ((t * fps + 1) // 3)
# print(f"start:{start}, end:{end}")
# 前进段
for j in range(start, end):
    angle = j * (s_theta_f / end)
    vehicle_x = center_x + radius * np.cos(angle)
    vehicle_y = center_y + radius * np.sin(angle)
    vehicle_theta = (angle + np.pi / 2) % (2 * np.pi)  # 切线方向
    # vehicle_pose.append([vehicle_x, vehicle_y, vehicle_theta])

# 后退段
angle_temp = vehicle_pose[-1][2] - np.pi / 2 + np.pi
center_x = 2 * radius * np.cos(vehicle_pose[-1][2]- np.pi / 2)
center_y = 2 * radius * np.sin(vehicle_pose[-1][2]- np.pi / 2)
# print(f"x:{center_x}, y:{center_y}")
for j in range(start, end):
    angle = angle_temp + j * (s_theta_r / end)
    vehicle_x = center_x + radius * np.cos(angle)
    vehicle_y = center_y + radius * np.sin(angle)
    vehicle_theta = (angle - np.pi / 2) % (2 * np.pi)  # 切线反方向
    # vehicle_pose.append([vehicle_x, vehicle_y, vehicle_theta])
"""

"""
    # 生成一段挪库路径
    pos:x, y, theta 车辆当前的姿态
    radius:车辆转弯半径
    is_fwd:是否是前进，当前两端，左转前进，右转后退
    angle:需要向前/向后运动的圆心角度
    veh_pose:输出，保存当前路径段的姿态点集
"""
def genarate_left_path(pos, radius, is_fwd, angle, veh_pose):
    t = 5
    fps = 30
    veh_x = pos[0]
    veh_y = pos[1]
    veh_theta = pos[2]

    if is_fwd:
        x_o = veh_x + radius * math.cos(veh_theta + math.pi / 2)
        y_o = veh_y + radius * math.sin(veh_theta + math.pi / 2)
        ang_start = veh_theta - math.pi / 2
    else:
        x_o = veh_x + radius * math.cos(veh_theta - math.pi / 2)
        y_o = veh_y + radius * math.sin(veh_theta - math.pi / 2)
        ang_start = veh_theta + math.pi / 2

    for i in range(t*fps + 1):
        ang_i = ang_start + i * angle / (t*fps + 1)
        vehicle_x = x_o + radius * np.cos(ang_i)
        vehicle_y = y_o + radius * np.sin(ang_i)
        if is_fwd:
            vehicle_theta = (ang_i + np.pi / 2) % (2 * np.pi)
        else:
            vehicle_theta = (ang_i - np.pi / 2) % (2 * np.pi)
        veh_pose.append([vehicle_x, vehicle_y, vehicle_theta])
    # print(len(veh_pose))

def genarate_left_path_one_step(pos, radius, is_fwd, angle, veh_pose):
    # t = 5
    # fps = 30
    veh_x = pos[0]
    veh_y = pos[1]
    veh_theta = pos[2]

    if is_fwd:
        x_o = veh_x + radius * math.cos(veh_theta + math.pi / 2)
        y_o = veh_y + radius * math.sin(veh_theta + math.pi / 2)
        ang_start = veh_theta - math.pi / 2
    else:
        x_o = veh_x + radius * math.cos(veh_theta - math.pi / 2)
        y_o = veh_y + radius * math.sin(veh_theta - math.pi / 2)
        ang_start = veh_theta + math.pi / 2

    # for i in range(t*fps + 1):
    ang_i = ang_start + angle
    vehicle_x = x_o + radius * np.cos(ang_i)
    vehicle_y = y_o + radius * np.sin(ang_i)
    if is_fwd:
        vehicle_theta = (ang_i + np.pi / 2) % (2 * np.pi)
    else:
        vehicle_theta = (ang_i - np.pi / 2) % (2 * np.pi)
    veh_pose.append([vehicle_x, vehicle_y, vehicle_theta])
    # print(len(veh_pose))


def genarate_right_path(pos, radius, is_fwd, angle, veh_pose):
    t = 5
    fps = 30
    veh_x = pos[0]
    veh_y = pos[1]
    veh_theta = pos[2]

    if is_fwd:
        x_o = veh_x + radius * math.cos(veh_theta - math.pi / 2)
        y_o = veh_y + radius * math.sin(veh_theta - math.pi / 2)
        ang_start = veh_theta + math.pi / 2
    else:
        x_o = veh_x + radius * math.cos(veh_theta + math.pi / 2)
        y_o = veh_y + radius * math.sin(veh_theta + math.pi / 2)
        ang_start = veh_theta - math.pi / 2

    for i in range(t*fps + 1):
        ang_i = ang_start - i * angle / (t*fps + 1)
        vehicle_x = x_o + radius * np.cos(ang_i)
        vehicle_y = y_o + radius * np.sin(ang_i)
        if is_fwd:
            vehicle_theta = (ang_i - np.pi / 2) % (2 * np.pi)
        else:
            vehicle_theta = (ang_i + np.pi / 2) % (2 * np.pi)
        veh_pose.append([vehicle_x, vehicle_y, vehicle_theta])
    # print(len(veh_pose))

def genarate_right_path_one_step(pos, radius, is_fwd, angle, veh_pose):
    # t = 5
    # fps = 30
    veh_x = pos[0]
    veh_y = pos[1]
    veh_theta = pos[2]

    if is_fwd:
        x_o = veh_x + radius * math.cos(veh_theta - math.pi / 2)
        y_o = veh_y + radius * math.sin(veh_theta - math.pi / 2)
        ang_start = veh_theta + math.pi / 2
    else:
        x_o = veh_x + radius * math.cos(veh_theta + math.pi / 2)
        y_o = veh_y + radius * math.sin(veh_theta + math.pi / 2)
        ang_start = veh_theta - math.pi / 2

    # for i in range(t*fps + 1):
    ang_i = ang_start - angle
    vehicle_x = x_o + radius * np.cos(ang_i)
    vehicle_y = y_o + radius * np.sin(ang_i)
    if is_fwd:
        vehicle_theta = (ang_i - np.pi / 2) % (2 * np.pi)
    else:
        vehicle_theta = (ang_i + np.pi / 2) % (2 * np.pi)
    veh_pose.append([vehicle_x, vehicle_y, vehicle_theta])
    # print(len(veh_pose))


# 车辆顶点计算（以后轴中心为参考）
def get_car_corners(x, y, theta):
    # 后轴中心是 (x, y)，向前 dx，向左右 dy
    corners = np.array([
        [RF, -W_2],     # front right
        [RF, W_2],      # front left
        [-RB, W_2],     # rear left
        [-RB, -W_2],    # rear right
    ])
    rot = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)],
    ])
    rotated = corners @ rot.T
    return rotated + np.array([x, y])

root = tk.Tk()
root.title("Vehicle Kinematics.")

# 设置绘图
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.grid(True)
ax.set_xlim(-15, radius + 5)
ax.set_ylim(-radius - 5, radius + 5)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 初始化车辆轮廓和轨迹
# closed=True 表示这个多边形是闭合的（最后一个点和第一个点之间会自动连接）
# fc 是 "face color"（填充颜色）的缩写，设置车身为蓝色
# alpha=0.7 设置透明度，范围是 0 到 1，值越小越透明
car_patch = Polygon(np.zeros((4, 2)), closed=True, fc='blue', alpha=0.7)
ax.add_patch(car_patch)
car_init_patch = Polygon(np.zeros((4, 2)), closed=True, fc='blue', alpha=0.5)
ax.add_patch(car_init_patch)
center_trajectory, = ax.plot([], [], 'g--')  # 后轴中心点轨迹
fr_trajectory, = ax.plot([], [], 'g--')  # 右前角点轨迹
fl_trajectory, = ax.plot([], [], 'g--')  # 左前角点轨迹
rl_trajectory, = ax.plot([], [], 'g--')  # 左后角点轨迹
rr_trajectory, = ax.plot([], [], 'g--')  # 右后角点轨迹

# 画车位边界
ps_width = 2.1
ps_length = 6.0
ps_buf = 5
ps_x = [-(ps_length + ps_buf), -ps_length, -ps_length, 0, 0, ps_buf]
ps_y = [0, 0, -ps_width, -ps_width, 0, 0]
parking_space, = ax.plot(ps_x, ps_y, 'r', label='Static Line')

# 记录轨迹
center_x_traj, center_y_traj = [], []
fr_x_traj, fr_y_traj = [], []
fl_x_traj, fl_y_traj = [], []
rl_x_traj, rl_y_traj = [], []
rr_x_traj, rr_y_traj = [], []

init_pos_show = tk.BooleanVar(value=False)
vehicle_show = tk.BooleanVar(value=True)
center_show_traj = tk.BooleanVar(value=True)
fr_show_traj = tk.BooleanVar(value=True)
fl_show_traj = tk.BooleanVar(value=True)
rl_show_traj = tk.BooleanVar(value=True)
rr_show_traj = tk.BooleanVar(value=True)

# 控制面板
control_frame = tk.Frame(root)
control_frame.pack(side=tk.RIGHT, fill=tk.Y)

def on_checkbox_toggle_init_pos():
    if not vehicle_pose:
        return

    init_corners = get_car_corners(vehicle_pose[0][0], vehicle_pose[0][1], vehicle_pose[0][2])
    # 每次勾选切换时更新一次轨迹显示
    if init_pos_show.get():
        car_init_patch.set_visible(True)
        car_init_patch.set_xy(init_corners)
    else:
        car_init_patch.set_visible(False)
    # 刷新图像显示的函数
    canvas.draw_idle()

def on_checkbox_toggle_vehicle_show():
    # 每次勾选切换时更新一次轨迹显示
    if vehicle_show.get():
        car_patch.set_visible(True)
        car_patch.set_xy(corners)
    else:
        car_patch.set_visible(False)
    # 刷新图像显示的函数
    canvas.draw_idle()

def on_checkbox_toggle_center_traj():
    # 每次勾选切换时更新一次轨迹显示
    if center_show_traj.get():
        center_trajectory.set_data(center_x_traj, center_y_traj)
    else:
        center_trajectory.set_data([], [])
    # 刷新图像显示的函数
    canvas.draw_idle()

def on_checkbox_toggle_fr_traj():
    # 每次勾选切换时更新一次轨迹显示
    if fr_show_traj.get():
        fr_trajectory.set_data(fr_x_traj, fr_y_traj)
    else:
        fr_trajectory.set_data([], [])
    canvas.draw_idle()

def on_checkbox_toggle_fl_traj():
    # 每次勾选切换时更新一次轨迹显示
    if fl_show_traj.get():
        fl_trajectory.set_data(fl_x_traj, fl_y_traj)
    else:
        fl_trajectory.set_data([], [])
    canvas.draw_idle()

def on_checkbox_toggle_rl_traj():
    # 每次勾选切换时更新一次轨迹显示
    if rl_show_traj.get():
        rl_trajectory.set_data(rl_x_traj, rl_y_traj)
    else:
        rl_trajectory.set_data([], [])
    canvas.draw_idle()

def on_checkbox_toggle_rr_traj():
    # 每次勾选切换时更新一次轨迹显示
    if rr_show_traj.get():
        rr_trajectory.set_data(rr_x_traj, rr_y_traj)
    else:
        rr_trajectory.set_data([], [])
    canvas.draw_idle()

init_pos_check = tk.Checkbutton(control_frame, text="init pos", variable=init_pos_show, command=on_checkbox_toggle_init_pos)
init_pos_check.pack(pady=10)
vehicle_check = tk.Checkbutton(control_frame, text="veh show", variable=vehicle_show, command=on_checkbox_toggle_vehicle_show)
vehicle_check.pack(pady=10)
center_check = tk.Checkbutton(control_frame, text="center traj", variable=center_show_traj, command=on_checkbox_toggle_center_traj)
center_check.pack(pady=10)
fr_check = tk.Checkbutton(control_frame, text="fr traj", variable=fr_show_traj, command=on_checkbox_toggle_fr_traj)
fr_check.pack(pady=10)
fl_check = tk.Checkbutton(control_frame, text="fl traj", variable=fl_show_traj, command=on_checkbox_toggle_fl_traj)
fl_check.pack(pady=10)
rl_check = tk.Checkbutton(control_frame, text="rl traj", variable=rl_show_traj, command=on_checkbox_toggle_rl_traj)
rl_check.pack(pady=10)
rr_check = tk.Checkbutton(control_frame, text="rr traj", variable=rr_show_traj, command=on_checkbox_toggle_rr_traj)
rr_check.pack(pady=10)

# 动画函数
def update(frame, pose):
    # frame 是当前动画的第几帧（从 0 开始）；

    center_x = pose[frame][0]
    center_y = pose[frame][1]
    center_theta = pose[frame][2]

    # 更新车辆轮廓
    global corners
    corners = get_car_corners(center_x, center_y, center_theta)
    # 车辆右前点
    point_fr = corners[0]
    # print(f"fr_x = {point_fr[0]}")

    if vehicle_show.get():
        car_patch.set_xy(corners)

    # 更新轨迹
    center_x_traj.append(center_x)
    center_y_traj.append(center_y)
    fr_x_traj.append(corners[0, 0])
    fr_y_traj.append(corners[0, 1])
    fl_x_traj.append(corners[1, 0])
    fl_y_traj.append(corners[1, 1])
    rl_x_traj.append(corners[2, 0])
    rl_y_traj.append(corners[2, 1])
    rr_x_traj.append(corners[3, 0])
    rr_y_traj.append(corners[3, 1])

    if center_show_traj.get():
        center_trajectory.set_data(center_x_traj, center_y_traj)
    # trajectory.set_visible(show_trajectory[0])
    if fr_show_traj.get():
        fr_trajectory.set_data(fr_x_traj, fr_y_traj)
    # trajectory.set_visible(show_trajectory[0])
    if fl_show_traj.get():
        fl_trajectory.set_data(fl_x_traj, fl_y_traj)
    if rl_show_traj.get():
        rl_trajectory.set_data(rl_x_traj, rl_y_traj)
    if rr_show_traj.get():
        rr_trajectory.set_data(rr_x_traj, rr_y_traj)
        
    return car_patch, center_trajectory, fr_trajectory, fl_trajectory, rl_trajectory, rr_trajectory

safe_buf = 0.15
# 车辆起始点，车尾距离车位边界safe_buf
vehicle_pose.append([-ps_length + safe_buf + RB, -W_2, 0])
# corners = get_car_corners(center_x, center_y, center_theta)
# car_patch.set_xy(corners)
is_fwd = True
while True:
    v_pose = [vehicle_pose[-1][0], vehicle_pose[-1][1], vehicle_pose[-1][2]]
    veh_corners = get_car_corners(v_pose[0], v_pose[1], v_pose[2])
    
    if is_fwd:
        # 前进判断右前角点是否安全
        if(veh_corners[0][0] > -safe_buf):
            is_fwd = not is_fwd
    else:
        # 后退判断左后角点是否安全
        if(ps_length + veh_corners[2][0] < safe_buf):
            is_fwd = not is_fwd
    
    # 右前角点出车位
    if veh_corners[0][1] > 0 + safe_buf:
        break

    angle = 0.05/5.68
    genarate_left_path_one_step(v_pose, 5.68, is_fwd, angle, vehicle_pose)

print(f"vehicle_pose size : {len(vehicle_pose)}")

# for i in range(24):
#     v_pose = [vehicle_pose[-1][0], vehicle_pose[-1][1], vehicle_pose[-1][2]]

#     if i % 2 == 0:
#         is_fwd = True
#     else:
#         is_fwd = False

#     angle = 1.5/5.68
#     genarate_right_path(v_pose, 5.68, is_fwd, angle, vehicle_pose)

# 创建动画
# repeat=False 取消循环播放
anim = FuncAnimation(fig, partial(update, pose=vehicle_pose), frames=len(vehicle_pose), interval=1000/fps, blit=True, repeat=False)
# 启动
root.mainloop()
# plt.title("Car Moving Along a Circular Trajectory")
# plt.show()
