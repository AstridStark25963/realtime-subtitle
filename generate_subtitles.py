import os
from datetime import timedelta
from tqdm import tqdm  # 引入 tqdm 进度条库

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

def generate_srt_with_timestamps(mapped_sentences, base_name):
    """生成 SRT 字幕文件"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    srt_path = os.path.join(OUTPUT_DIR, f"{base_name}.srt")

    def format_timestamp(seconds):
        milliseconds = int((seconds % 1) * 1000)
        time = str(timedelta(seconds=int(seconds))).zfill(8)
        return f"{time},{milliseconds:03d}"

    print("Generating SRT file...")
    with open(srt_path, "w", encoding="utf-8") as srt_file:
        with tqdm(total=len(mapped_sentences), desc="Writing subtitles", unit="subtitle") as pbar:
            for idx, sentence in enumerate(mapped_sentences, 1):
                start_time = format_timestamp(sentence["start"])
                end_time = format_timestamp(sentence["end"])
                srt_file.write(f"{idx}\n")
                srt_file.write(f"{start_time} --> {end_time}\n")
                srt_file.write(f"{sentence['text']}\n\n")
                pbar.update(1)

    print(f"SRT file saved to: {srt_path}")
