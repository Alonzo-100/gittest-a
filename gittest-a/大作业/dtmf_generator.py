import numpy as np
import soundfile as sf

# DTMF 频率对照表（和你识别程序完全一致）
DTMF_FREQ = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '0': (941, 1336), '*': (941, 1477), '#': (941, 1633)
}

# 参数（和识别端匹配）
SAMPLE_RATE = 8000
TONE_DURATION = 0.3       # 每个按键发声时长
GAP_DURATION = 0.2         # 按键之间静音间隔
AMPLITUDE = 0.4            # 音量，避免削波失真

def generate_dtmf_tone(digit, sr, duration, amp):
    """生成单个DTMF按键波形"""
    f_low, f_high = DTMF_FREQ[digit]
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    tone = amp * (np.sin(2 * np.pi * f_low * t) + np.sin(2 * np.pi * f_high * t))
    return tone

def generate_dtmf_sequence(phone_str, save_path="dtmf_dial.wav"):
    """生成一串拨号音频并保存wav"""
    full_audio = np.array([], dtype=np.float32)
    gap_samples = int(SAMPLE_RATE * GAP_DURATION)
    silence = np.zeros(gap_samples, dtype=np.float32)

    for ch in phone_str:
        if ch not in DTMF_FREQ:
            print(f"跳过无效字符：{ch}")
            continue
        tone = generate_dtmf_tone(ch, SAMPLE_RATE, TONE_DURATION, AMPLITUDE)
        full_audio = np.concatenate([full_audio, tone, silence])

    sf.write(save_path, full_audio, SAMPLE_RATE)
    print(f"DTMF音频已生成：{save_path}")
    print(f"拨号内容：{phone_str}")

if __name__ == "__main__":
    # 修改号码
    dial_number = "13023732659"
    generate_dtmf_sequence(dial_number, "dial_test.wav")