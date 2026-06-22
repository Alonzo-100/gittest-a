import sys
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QPushButton, QTextEdit, QHBoxLayout)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# 解决中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class SignalGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("离散信号显示 GUI")
        self.resize(900, 600)
        self.initUI()
        self.show_step()  # 默认显示阶跃信号

    def initUI(self):
        main = QWidget()
        self.setCentralWidget(main)
        layout = QHBoxLayout(main)

        # 左侧面板
        left = QWidget()
        left.setFixedWidth(260)
        vbox = QVBoxLayout(left)

        # 只保留3个按钮
        self.btn1 = QPushButton("单位脉冲信号")
        self.btn2 = QPushButton("单位阶跃信号")
        self.btn3 = QPushButton("正弦离散信号")

        self.btn1.clicked.connect(self.show_impulse)
        self.btn2.clicked.connect(self.show_step)
        self.btn3.clicked.connect(self.show_sin)

        self.info = QTextEdit()
        self.info.setReadOnly(True)

        vbox.addWidget(self.btn1)
        vbox.addWidget(self.btn2)
        vbox.addWidget(self.btn3)
        vbox.addWidget(self.info)

        # 右侧绘图
        self.fig, self.ax = plt.subplots(figsize=(6,4), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(left)
        layout.addWidget(self.canvas)

    def draw(self, n, x, title):
        self.ax.clear()
        self.ax.stem(n, x, linefmt='r-', markerfmt='ro', basefmt=' ')
        self.ax.set_title(title)
        self.ax.set_xlabel("n")
        self.ax.set_ylabel("x(n)")
        self.ax.grid(True)
        self.ax.set_ylim(-0.2, 1.2)
        self.canvas.draw()

    # 1. 单位脉冲信号
    def show_impulse(self):
        n = np.arange(-5,6)
        x = np.where(n==0, 1, 0)
        self.draw(n, x, "单位脉冲信号 δ(n)")
        self.info.setPlainText("单位脉冲信号：仅在n=0时取值为1，其余时刻为0，是离散系统最基础信号。")

    # 2. 单位阶跃信号
    def show_step(self):
        n = np.arange(-5,6)
        x = np.where(n>=0, 1, 0)
        self.draw(n, x, "单位阶跃信号 u(n)")
        self.info.setPlainText("单位阶跃信号：n≥0时为1，n<0时为0，常用于表示信号的起始与开关控制。")

    # 3. 正弦离散信号
    def show_sin(self):
        n = np.arange(0,20)
        x = np.sin(np.pi/6 * n)
        self.draw(n, x, "正弦离散信号 sin(πn/6)")
        self.info.setPlainText("正弦离散信号：按正弦规律周期振荡，用于频率分析、滤波与系统测试。")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SignalGUI()
    w.show()
    sys.exit(app.exec())