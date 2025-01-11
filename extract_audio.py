import os
import tkinter as tk
from tkinter import filedialog
import subprocess
from datetime import datetime

FFMPEG_PATH = os.path.join(os.path.dirname(__file__), "tools", "ffmpeg", "ffmpeg.exe")
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")  # 临时文件夹

def select_video_file():
    """打开文件选择窗口，选择视频文件"""
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])
    return filepath if filepath else None

def generate_output_filename(video_file):
    """生成音频文件名，格式为：视频名称 + 时间戳"""
    os.makedirs(TEMP_DIR, exist_ok=True)
    video_name = os.path.splitext(os.path.basename(video_file))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(TEMP_DIR, f"{video_name}_{timestamp}.wav")

def extract_audio(video_file):
    """提取视频中的音频"""
    try:
        output_path = generate_output_filename(video_file)
        command = [
            FFMPEG_PATH, "-i", video_file, "-vn",
            "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", output_path
        ]
        subprocess.run(command, check=True)
        log(f"Audio extracted to: {output_path}")
        print("Audio extraction completed successfully.")
        return output_path
    except subprocess.CalledProcessError as e:
        log(f"Error extracting audio: {e}")
        return None

def log(message):
    """写入日志文件"""
    with open("process.log", "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

def main():
    video_file = select_video_file()
    if video_file:
        extract_audio(video_file)

if __name__ == "__main__":
    main()
