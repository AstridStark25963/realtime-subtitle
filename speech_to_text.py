from vosk import Model, KaldiRecognizer
import wave
import json
import os
from datetime import datetime
from deepmultilingualpunctuation import PunctuationModel
from tqdm import tqdm  # 引入 tqdm 进度条库
import re

MODEL_DIR = os.path.join(os.path.dirname(__file__), "tools", "models")
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")

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
    words = []

    with wave.open(audio_file, "rb") as wf:
        total_frames = wf.getnframes()
        with tqdm(total=total_frames, desc="Processing audio", unit="frames") as pbar:
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    words.extend(result.get("result", []))
                pbar.update(4000)
    return words

def clean_sentence(sentence):
    """清理句子末尾的标点符号，不影响单词内的标点符号"""
    return re.sub(r'[^\w\s]*$', '', sentence)

def split_sentences_with_punctuation(text):
    """使用标点符号分句，支持句号、逗号、分号等"""
    sentences = re.split(r'(?<=[.?!,;])\s*', text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

def punctuate_and_split(text):
    """使用 DeepMultilingualPunctuation 添加标点，并基于标点符号分句"""
    punctuation_model = PunctuationModel()
    print("Adding punctuation and splitting sentences...")
    punctuated_text = punctuation_model.restore_punctuation(text)
    sentences = split_sentences_with_punctuation(punctuated_text)
    cleaned_sentences = [clean_sentence(sentence) for sentence in sentences]
    return cleaned_sentences

def map_sentences_to_timestamps(words, sentences):
    """将分句结果映射到时间戳"""
    mapped_sentences = []
    start_idx = 0

    print("Mapping sentences to timestamps...")
    with tqdm(total=len(sentences), desc="Mapping sentences", unit="sentence") as pbar:
        for sentence in sentences:
            sentence_words = sentence.split()
            sent_start_word = sentence_words[0]
            sent_end_word = sentence_words[-1]

            sent_start_time = None
            sent_end_time = None

            for idx, word in enumerate(words[start_idx:], start=start_idx):
                if word["word"] == sent_start_word and sent_start_time is None:
                    sent_start_time = word["start"]
                if word["word"] == sent_end_word:
                    sent_end_time = word["end"]
                    start_idx = idx + 1
                    break

            if sent_start_time is not None and sent_end_time is not None:
                mapped_sentences.append({
                    "text": sentence,
                    "start": sent_start_time,
                    "end": sent_end_time
                })
            pbar.update(1)

    return mapped_sentences

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
        words = recognize_audio_with_timestamps(model, audio_file)
        log(f"Recognition completed for audio: {audio_file}")

        # 提取识别文本
        text = " ".join([word["word"] for word in words])

        # 分句并添加标点
        sentences = punctuate_and_split(text)

        # 映射时间戳
        mapped_sentences = map_sentences_to_timestamps(words, sentences)
        log(f"Mapping completed for audio: {audio_file}")

        # 返回映射结果和基础文件名
        print("Recognition and mapping completed successfully.")
        return mapped_sentences, base_name

    except Exception as e:
        log(f"Error: {e}")
        print("An error occurred. Check the log file for details.")

if __name__ == "__main__":
    main()
