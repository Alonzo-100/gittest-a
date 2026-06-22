import sys
import numpy as np
import sounddevice as sd
import soundfile as sf
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLineEdit, QPushButton, QLabel, QTextEdit)
from PyQt6.QtCore import Qt

# DTMF 频率配置
DTMF_FREQ = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477)
}
SAMPLE_RATE = 8000
TONE_DURATION = 0.2
GAP_DURATION = 0.1
AMPLITUDE = 0.5

def generate_dtmf_audio(phone_num):
    """生成DTMF音频波形"""
    audio_data = np.array([], dtype=np.float32)
    t_tone = np.linspace(0, TONE_DURATION, int(SAMPLE_RATE * TONE_DURATION), endpoint=False)
    t_gap = np.zeros(int(SAMPLE_RATE * GAP_DURATION), dtype=np.float32)

    for char in phone_num:
        if char not in DTMF_FREQ:
            continue
        f1, f2 = DTMF_FREQ[char]
        tone = AMPLITUDE * (np.sin(2 * np.pi * f1 * t_tone) + np.sin(2 * np.pi * f2 * t_tone))
        audio_data = np.concatenate([audio_data, tone, t_gap])
    return audio_data

class DTMFWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DTMF 音频生成工具")
        self.setFixedSize(420, 280)
        self.audio_cache = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # 输入区域
        self.label = QLabel("输入号码（支持 0-9 * #）：")
        self.edit_num = QLineEdit()
        self.edit_num.setPlaceholderText("例如：123456 *#")

        # 功能按钮
        self.btn_play = QPushButton("生成并播放音频")
        self.btn_save = QPushButton("保存为 WAV 文件")

        # 日志输出
        self.log_label = QLabel("运行日志：")
        self.text_log = QTextEdit()
        self.text_log.setReadOnly(True)

        # 绑定事件
        self.btn_play.clicked.connect(self.play_audio)
        self.btn_save.clicked.connect(self.save_audio)

        # 布局添加控件
        layout.addWidget(self.label)
        layout.addWidget(self.edit_num)
        layout.addWidget(self.btn_play)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.log_label)
        layout.addWidget(self.text_log)

    def add_log(self, msg):
        self.text_log.append(msg)

    def play_audio(self):
        num = self.edit_num.text().strip()
        if not num:
            self.add_log("提示：请先输入号码！")
            return
        self.audio_cache = generate_dtmf_audio(num)
        self.add_log(f"已生成号码 [{num}] 的音频，开始播放")
        sd.play(self.audio_cache, samplerate=SAMPLE_RATE)

    def save_audio(self):
        if self.audio_cache is None:
            self.add_log("提示：请先生成音频！")
            return
        save_path = "dtmf_output.wav"
        sf.write(save_path, self.audio_cache, SAMPLE_RATE)
        self.add_log(f"音频已保存到：{save_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DTMFWindow()
    win.show()
    sys.exit(app.exec())
    