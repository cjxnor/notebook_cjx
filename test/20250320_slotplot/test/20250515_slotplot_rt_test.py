# -*- coding: utf-8 -*-
# 绘制动图
import json
from datetime import datetime
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
    tdata = {}
    tstamp = []

    # 转换为 datetime 对象（注意毫秒是 `%f`，字符串中是三位数）
    time_format = "%Y%m%d %H:%M:%S.%f"
    tdata_temp = []
    for entry in data:
        nowt_str = entry["timestamp"]
        nowt = datetime.strptime(nowt_str, time_format)
        if not tdata_temp:
            tdata_temp.append(entry)
            tstamp.append(nowt_str)
        else:
            lastt_str = tdata_temp[-1]["timestamp"]
            lastt = datetime.strptime(lastt_str, time_format)
            # 计算时间差（timedelta 对象）
            deltat = abs(nowt - lastt)
            # 判断是否大于 1 秒
            if deltat.total_seconds() > 1:
                tdata[tdata_temp[0]["timestamp"]] = tdata_temp
                tstamp.append(nowt_str)
                tdata_temp = []
                tdata_temp.append(entry)
            else:
                tdata_temp.append(entry)

    if tdata_temp:
        tdata[tdata_temp[0]["timestamp"]] = tdata_temp

    return tdata, tstamp


# 📌 读取 JSON 文件
current_dir = os.getcwd()  # 获取当前工作目录
print(f"pwd : {current_dir}")
file_path = os.path.join(current_dir, 'test/20250320_slotplot/test/20250514_pdc_slot_rt_test.json')  # 拼接成 data 目录路径
data_temp = read_json_lines(file_path)
json_data, timestamps = get_timestamps(data_temp)
# global sorted_timestamps
sorted_timestamps = sorted(timestamps)

print(f"data_temp : {len(json_data)}, timestamps : {len(timestamps)}")

# for i in range(len(json_data)):
#     print(f"{json_data[i][0]["timestamp"]}")

for k, v in json_data.items():
    print(f"{k}")

print("-----")

for i in range(len(timestamps)):
    print(f"{timestamps[i]}")
    print(f"{json_data[timestamps[i]][0]}")

