import numpy as np
import scipy.io.wavfile as wav
import scipy.fftpack as fft
import tkinter as tk
from tkinter import filedialog, messagebox

# DTMF 频率表（行频率 + 列频率）
DTMF_FREQS = {
    (697, 1209): '1', (697, 1336): '2', (697, 1477): '3',
    (770, 1209): '4', (770, 1336): '5', (770, 1477): '6',
    (852, 1209): '7', (852, 1336): '5', (852, 1477): '9',
    (941, 1209): '*', (941, 1336): '0', (941, 1477): '#'
}

# 标准频率列表（用于匹配检测）
ROW_FREQS = [697, 770, 852, 941]
COL_FREQS = [1209, 1336, 1477]

def detect_dtmf(audio_data, sample_rate):
    """检测音频中的DTMF拨号音，返回识别的号码"""
    # 预处理：取单声道、归一化
    if len(audio_data.shape) > 1:
        audio_data = audio_data[:, 0]
    audio_data = audio_data / np.max(np.abs(audio_data))
    
    # 分帧处理（每帧20ms，适合DTMF检测）
    frame_size = int(0.02 * sample_rate)
    hop_size = int(0.01 * sample_rate)
    frames = []
    
    for i in range(0, len(audio_data) - frame_size, hop_size):
        frames.append(audio_data[i:i+frame_size])
    
    detected_digits = []
    last_digit = None
    
    for frame in frames:
        # FFT变换获取频谱
        yf = fft.fft(frame)
        xf = fft.fftfreq(len(frame), 1 / sample_rate)
        yf = np.abs(yf[:len(frame)//2])
        xf = xf[:len(frame)//2]
        
        # 找峰值频率
        row_freq = find_closest_freq(xf, yf, ROW_FREQS)
        col_freq = find_closest_freq(xf, yf, COL_FREQS)
        
        if row_freq and col_freq:
            digit = DTMF_FREQS.get((row_freq, col_freq))
            if digit and digit != last_digit:
                detected_digits.append(digit)
                last_digit = digit
    
    return ''.join(detected_digits)

def find_closest_freq(freqs, power, target_freqs):
    """找到最接近目标频率的峰值"""
    threshold = np.max(power) * 0.1  # 能量阈值
    for f in target_freqs:
        idx = np.argmin(np.abs(freqs - f))
        if power[idx] > threshold:
            return f
    return None

class DTMFDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DTMF拨号音号码识别器")
        self.root.geometry("500x300")
        
        # 变量
        self.file_path = tk.StringVar()
        self.result = tk.StringVar(value="识别结果：")
        
        # GUI组件
        tk.Label(root, text="DTMF音频拨号键识别", font=("Arial", 16)).pack(pady=10)
        
        tk.Button(root, text="选择音频文件", command=self.load_file, width=15).pack(pady=5)
        tk.Entry(root, textvariable=self.file_path, width=40, state="readonly").pack(pady=5)
        
        tk.Button(root, text="开始识别", command=self.recognize, width=15, bg="#4CAF50", fg="white").pack(pady=10)
        
        tk.Label(root, textvariable=self.result, font=("Arial", 14), fg="blue").pack(pady=5)
        
        tk.Label(root, text="支持格式：WAV音频文件", font=("Arial", 10)).pack(side=tk.BOTTOM, pady=10)
    
    def load_file(self):
        """加载音频文件"""
        path = filedialog.askopenfilename(
            title="选择DTMF拨号音文件",
            filetypes=[("WAV音频文件", "*.wav"), ("所有文件", "*.*")]
        )
        if path:
            self.file_path.set(path)
            self.result.set("识别结果：")
    
    def recognize(self):
        """识别号码"""
        path = self.file_path.get()
        if not path:
            messagebox.showerror("错误", "请先选择音频文件！")
            return
        
        try:
            # 读取音频
            sample_rate, audio_data = wav.read(path)
            # 识别
            digits = detect_dtmf(audio_data, sample_rate)
            # 显示结果
            if digits:
                self.result.set(f"识别结果：{digits}")
                messagebox.showinfo("成功", f"识别完成！\n号码：{digits}")
            else:
                self.result.set("识别结果：未检测到号码")
                messagebox.showwarning("提示", "未识别到有效DTMF信号")
        except Exception as e:
            messagebox.showerror("错误", f"识别失败：{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DTMFDetectorGUI(root)
    root.mainloop()
    