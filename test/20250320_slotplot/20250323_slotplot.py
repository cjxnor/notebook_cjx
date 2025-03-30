import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QMenuBar, QAction, QFileDialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from collections import defaultdict

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.json_data = []
        self.fig = None
        self.pdc_psolt_id = ""
        self.pcd_psolt_latreftype = ""
        self.pcd_psolt_slottype = ""
        self.PDC_PSolt_attribute_Status = ""

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Draw Slot")
        self.setGeometry(100, 100, 1000, 800)
        
        # Central widget and layout
        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)

        # Label for additional information
        self.label = QLabel(self)
        central_layout.addWidget(self.label)

        # Combobox for timestamps
        self.timestamp_combobox = QComboBox(self)
        self.timestamp_combobox.currentIndexChanged.connect(self.on_timestamp_selected)
        central_layout.addWidget(self.timestamp_combobox)

        # Matplotlib canvas
        self.canvas = FigureCanvas(plt.figure())
        central_layout.addWidget(self.canvas)

        self.setCentralWidget(central_widget)

        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')

        open_action = QAction('打开 JSON 文件', self)
        open_action.triggered.connect(self.open_json_file)
        file_menu.addAction(open_action)

        save_action = QAction('保存图片', self)
        save_action.triggered.connect(self.save_plot)
        file_menu.addAction(save_action)

        exit_action = QAction('退出', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def read_json_lines(self, file_path):
        data = []
        with open(file_path, "r") as file:
            for line in file:
                try:
                    json_obj = json.loads(line.strip())
                    data.append(json_obj)
                except json.JSONDecodeError:
                    print(f"⚠️ 无法解析行: {line}")
        return data

    def get_timestamps(self, data):
        return list({entry["timestamp"] for entry in data})  # 去重

    def plot_coordinates(self, selected_timestamp):
        # 清除旧的图形
        self.fig.clf()
        ax = self.fig.add_subplot(111)

        # 过滤出选中的 timestamp 对应的坐标点
        filtered_data = [entry for entry in self.json_data if entry["timestamp"] == selected_timestamp]
        
        if not filtered_data:
            print(f"⚠️ 没有找到 timestamp: {selected_timestamp}")
            return
        
        # 提取坐标点
        indexs = ["obj1start_pos", "obj1end_pos", "slotobjstartpt_pos", "slotobjendpt_pos", "obj2start_pos", "obj2end_pos"]
        x_coords = [filtered_data[0][i]["x"] for i in indexs]
        y_coords = [filtered_data[0][i]["y"] for i in indexs]
        points_status = [filtered_data[0][i]["point_status"] for i in indexs]

        # 获取并更新显示信息
        self.pdc_psolt_id = filtered_data[0]["pdc_psolt_id"]
        self.pcd_psolt_latreftype = filtered_data[0]["pcd_psolt_latreftype"]
        self.pcd_psolt_slottype = filtered_data[0]["pcd_psolt_slottype"]
        self.PDC_PSolt_attribute_Status = filtered_data[0]["PDC_PSolt_attribute_Status"]

        self.label.setText(f"pdc_psolt_id: {self.pdc_psolt_id}\n"
                           f"pcd_psolt_latreftype: {self.pcd_psolt_latreftype}\n"
                           f"pcd_psolt_slottype: {self.pcd_psolt_slottype}\n"
                           f"PDC_PSolt_attribute_Status: {self.PDC_PSolt_attribute_Status}")

        # 绘图
        ax.scatter(x_coords, y_coords, color="blue")
        
        point_counts = defaultdict(int)
        for i, (x, y, index, point_status) in enumerate(zip(x_coords, y_coords, indexs, points_status)):
            offset = point_counts[(x, y)] * 0.6  # 每个相同坐标的点向上偏移
            ax.text(x, y + offset, f"{index}: {point_status}\n({x:.2f}, {y:.2f})", fontsize=10, ha="right", va="bottom", color="red")
            point_counts[(x, y)] += 1

        # 固定 x, y 轴范围
        axis_buff = 2.0
        ax.set_xlim(min(min(x_coords) - axis_buff, -axis_buff), max(max(x_coords) + axis_buff, axis_buff))
        ax.set_ylim(min(min(y_coords) - axis_buff, -axis_buff), max(max(y_coords) + axis_buff, axis_buff))

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title(f"Points - {selected_timestamp}")
        ax.grid(True)

        self.canvas.draw()

    def on_timestamp_selected(self):
        selected_timestamp = self.timestamp_combobox.currentText()
        self.plot_coordinates(selected_timestamp)

    def open_json_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 JSON 文件", "", "JSON Files (*.json);;All Files (*)")
        if file_path:
            self.json_data = self.read_json_lines(file_path)
            timestamps = self.get_timestamps(self.json_data)
            sorted_timestamps = sorted(timestamps)
            self.timestamp_combobox.clear()
            self.timestamp_combobox.addItems(sorted_timestamps)
            self.timestamp_combobox.setCurrentIndex(0)  # 默认选中第一个
            self.plot_coordinates(sorted_timestamps[0])

    def save_plot(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存图片", "", "PNG Files (*.png);;JPEG Files (*.jpg);;PDF Files (*.pdf);;SVG Files (*.svg)")
        if file_path:
            self.fig.savefig(file_path, dpi=300, bbox_inches="tight")
            print(f"Saved: {file_path}")

# 运行应用
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
