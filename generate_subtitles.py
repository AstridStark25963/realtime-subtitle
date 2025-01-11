import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

def format_time(seconds):
    """将秒转换为 SRT 的时间格式：hh:mm:ss,ms"""
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def generate_srt_with_timestamps(timestamps, base_name):
    """根据时间戳生成 SRT 字幕文件"""
    output_path = os.path.join(OUTPUT_DIR, f"{base_name}.srt")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for i, item in enumerate(timestamps, 1):
            start_time = format_time(item["start"])
            end_time = format_time(item["end"])
            text = item["text"]
            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")
    print(f"SRT file saved to: {output_path}")
    return output_path
