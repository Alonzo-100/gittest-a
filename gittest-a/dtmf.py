import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, fftfreq

# ---------------------- DTMF 频率表 ----------------------
DTMF_TABLE = {
    (697, 1209): '1',
    (697, 1336): '2',
    (697, 1477): '3',
    (770, 1209): '4',
    (770, 1336): '5',
    (770, 1477): '6',
    (852, 1209): '7',
    (852, 1336): '8',
    (852, 1477): '9',
    (941, 1336): '0',
    (941, 1209): '*',
    (941, 1477): '#'
}

# 标准DTMF频率列表
LOW_FREQS = [697, 770, 852, 941]
HIGH_FREQS = [1209, 1336, 1477]
FREQ_TOLERANCE = 25  # 频率误差允许范围

# ---------------------- 核心识别函数 ----------------------
def recognize_dtmf_number(wav_path, frame_duration=0.1, step_duration=0.05):
    """
    从音频文件中识别DTMF号码
    :param wav_path: 音频文件路径
    :param frame_duration: 每帧时长（秒）
    :param step_duration: 帧步长（秒）
    :return: 识别到的号码字符串
    """
    # 读取音频
    sample_rate, data = wavfile.read(wav_path)
    if len(data.shape) > 1:
        data = data[:, 0]  # 取单声道

    frame_length = int(frame_duration * sample_rate)
    step_length = int(step_duration * sample_rate)
    number = ""
    last_digit = None

    # 分帧处理
    for i in range(0, len(data) - frame_length, step_length):
        frame = data[i:i+frame_length]
        # 加汉明窗减少频谱泄漏
        windowed = frame * np.hamming(len(frame))
        # FFT
        yf = fft(windowed)
        xf = fftfreq(len(windowed), 1 / sample_rate)[:len(windowed)//2]
        yf_abs = np.abs(yf[:len(windowed)//2])

        # 取前两个最大峰值频率
        peak_indices = np.argsort(yf_abs)[-2:]
        peak_freqs = xf[peak_indices]
        peak_freqs.sort()

        # 匹配低频和高频
        low = None
        high = None
        for f in peak_freqs:
            for lf in LOW_FREQS:
                if abs(f - lf) < FREQ_TOLERANCE:
                    low = lf
            for hf in HIGH_FREQS:
                if abs(f - hf) < FREQ_TOLERANCE:
                    high = hf

        # 匹配数字
        if low and high:
            digit = DTMF_TABLE.get((low, high))
            if digit and digit != last_digit:
                number += digit
                last_digit = digit

    return number if number else "未识别到有效号码"

# ---------------------- GUI界面 ----------------------
class DTMFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DTMF 拨号音识别工具")
        self.root.geometry("500x300")

        # 标题
        title_label = tk.Label(root, text="DTMF 拨号音识别", font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=20)

        # 文件选择区域
        frame = ttk.Frame(root)
        frame.pack(pady=10)

        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(frame, textvariable=self.path_var, width=40)
        path_entry.pack(side=tk.LEFT, padx=5)

        browse_btn = ttk.Button(frame, text="选择音频文件", command=self.browse_file)
        browse_btn.pack(side=tk.LEFT)

        # 识别按钮
        recognize_btn = ttk.Button(root, text="开始识别", command=self.start_recognize)
        recognize_btn.pack(pady=15)

        # 结果显示
        self.result_var = tk.StringVar()
        result_label = tk.Label(root, textvariable=self.result_var, font=("微软雅黑", 14), fg="blue")
        result_label.pack(pady=10)

    def browse_file(self):
        """选择wav文件"""
        path = filedialog.askopenfilename(
            title="选择拨号音文件",
            filetypes=[("WAV音频文件", "*.wav"), ("所有文件", "*.*")]
        )
        if path:
            self.path_var.set(path)

    def start_recognize(self):
        """开始识别"""
        file_path = self.path_var.get()
        if not file_path:
            messagebox.showwarning("警告", "请先选择音频文件！")
            return

        try:
            result = recognize_dtmf_number(file_path)
            self.result_var.set(f"识别结果：{result}")
        except Exception as e:
            messagebox.showerror("错误", f"识别失败：{str(e)}")

# ---------------------- 运行程序 ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = DTMFApp(root)
    root.mainloop()
    