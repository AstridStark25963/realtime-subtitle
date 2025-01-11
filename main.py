import os
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import speech_to_text
import generate_subtitles

FFMPEG_PATH = os.path.join(os.path.dirname(__file__), "tools", "ffmpeg", "ffmpeg.exe")
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")  # 临时文件夹
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")  # 输出文件夹

def log(message):
    """写入日志文件"""
    with open("process.log", "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

def select_video_file():
    """打开文件选择窗口，选择视频文件"""
    try:
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])
        if filepath:
            log(f"Video file selected: {filepath}")
            return filepath
        else:
            log("No video file selected.")
            print("No video file selected. Exiting process.")
            return None
    except Exception as e:
        log(f"Error selecting video file: {e}")
        raise

def generate_output_filename(video_file):
    """生成音频文件名，格式为：视频名称 + 时间戳"""
    try:
        os.makedirs(TEMP_DIR, exist_ok=True)
        video_name = os.path.splitext(os.path.basename(video_file))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(TEMP_DIR, f"{video_name}_{timestamp}.wav")
    except Exception as e:
        log(f"Error generating output filename: {e}")
        raise

def extract_audio(video_file):
    """提取视频中的音频"""
    try:
        output_path = generate_output_filename(video_file)
        command = [
            FFMPEG_PATH, "-i", video_file, "-vn",  # 输入视频，忽略视频流
            "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", output_path  # 输出为 WAV 格式
        ]
        subprocess.run(command, check=True)
        log(f"Audio extracted to: {output_path}")
        print("Audio extraction completed successfully.")
        return output_path
    except subprocess.CalledProcessError as e:
        log(f"Error extracting audio: {e}")
        print("Audio extraction failed. Check logs for details.")
        raise

def run_pipeline():
    """执行整个流程：提取音频、语音识别、生成字幕、删除临时音频"""
    try:
        # 选择视频文件
        video_file = select_video_file()
        if not video_file:
            return

        # 提取音频
        audio_file = extract_audio(video_file)
        if not audio_file:
            return

        # 执行语音识别并获取时间戳
        timestamps, base_name = speech_to_text.main()

        # 生成 SRT 字幕文件
        generate_subtitles.generate_srt_with_timestamps(timestamps, base_name)

        # 删除临时音频文件
        if os.path.exists(audio_file):
            os.remove(audio_file)
            log(f"Temporary audio file deleted: {audio_file}")
            print("Temporary audio file deleted.")
        else:
            log("No temporary audio file to delete.")
            print("No temporary audio file to delete.")

        print("Subtitle generation completed successfully.")
        log("Pipeline completed successfully.")

    except FileNotFoundError as e:
        log(f"File not found: {e}")
        print(f"File not found: {e}. Check logs for details.")
    except Exception as e:
        log(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}. Check logs for details.")

if __name__ == "__main__":
    run_pipeline()
