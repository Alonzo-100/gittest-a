# 导入库
import numpy as np
import matplotlib.pyplot as plt

# ===================== 1. 连续信号：余弦信号 =====================
# 生成时间范围（连续）
t = np.linspace(0, 2 * np.pi, 1000)  # 0~2π，1000个点
y_cos = np.cos(t)  # 余弦信号

# 绘制连续信号
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(t, y_cos, 'b-', linewidth=2, label='连续余弦信号')
plt.title('连续信号 - 余弦信号')
plt.xlabel('时间 t')
plt.ylabel('幅值')
plt.grid(True)
plt.legend()

# ===================== 2. 离散信号：离散余弦信号 =====================
n = np.arange(0, 15)  # 离散时间点：0~14
y_discrete = np.cos(0.5 * n)  # 离散余弦信号

plt.subplot(1, 2, 2)
plt.stem(n, y_discrete, 'r-', markerfmt='ro', label='离散余弦信号')
plt.title('离散信号 - 离散余弦信号')
plt.xlabel('时间 n')
plt.ylabel('幅值')
plt.grid(True)
plt.legend()

# 显示图像
plt.tight_layout()
plt.show()