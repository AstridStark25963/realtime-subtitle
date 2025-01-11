from vosk import Model, KaldiRecognizer
import wave
import json
import os
from datetime import datetime
from tqdm import tqdm  # 添加进度条库

MODEL_DIR = os.path.join(os.path.dirname(__file__), "tools", "models")
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

def list_models():
    """列出可用的语言模型"""
    return [name for name in os.listdir(MODEL_DIR) if os.path.isdir(os.path.join(MODEL_DIR, name))]

def choose_model():
    """让用户选择语言模型"""
    models = list_models()
    print("Available models:")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    choice = int(input("Select a model by number: ")) - 1
    return os.path.join(MODEL_DIR, models[choice])

def find_latest_audio():
    """查找 temp 文件夹中最新生成的音频文件"""
    files = [os.path.join(TEMP_DIR, f) for f in os.listdir(TEMP_DIR) if f.endswith(".wav")]
    if not files:
        raise FileNotFoundError("No audio files found in temp directory.")
    latest_file = max(files, key=os.path.getmtime)
    return latest_file, os.path.splitext(os.path.basename(latest_file))[0]  # 返回文件路径和基础名称

def recognize_audio_with_timestamps(model, audio_file):
    """使用 Vosk 模型识别音频"""
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)
    results = []

    with wave.open(audio_file, "rb") as wf:
        total_frames = wf.getnframes()  # 获取总帧数
        with tqdm(total=total_frames, desc="Processing audio", unit="frames") as pbar:
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    for word in result.get("result", []):
                        results.append({
                            "text": word["word"],
                            "start": word["start"],
                            "end": word["end"]
                        })
                pbar.update(4000)  # 更新进度条
    return results

def log(message):
    """写入日志文件"""
    with open("process.log", "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

def main():
    try:
        # 选择模型
        model_path = choose_model()
        model = Model(model_path)

        # 查找最新音频文件
        audio_file, base_name = find_latest_audio()

        # 执行语音识别
        timestamps = recognize_audio_with_timestamps(model, audio_file)
        log(f"Recognition completed for audio: {audio_file}")

        # 返回识别结果和基础文件名
        print("Recognition completed successfully.")
        return timestamps, base_name

    except Exception as e:
        log(f"Error: {e}")
        print("An error occurred. Check the log file for details.")
