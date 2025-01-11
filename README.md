# Realtime Subtitle Project

## 📖 Introduction

This project is designed to generate subtitles from videos using Python, FFmpeg, and Vosk for offline speech-to-text processing. It supports single-language and bilingual subtitle generation, allowing users to easily extract subtitles from any video.

---

## 🌟 Features

- Extract audio from video files.

- Perform offline speech-to-text processing with Vosk.

- Generate subtitles in SRT format.

- Support bilingual subtitle generation (e.g., Chinese and English).

- Easy-to-use interface with minimal configuration.


---

## 🔧 Requirements

- **Python** 3.12 or higher
- **FFmpeg** (bundled in `tools/ffmpeg/`)
- **Vosk** model files (bundled in `tools/models/`)

---

## 📂 Installation

1. Clone the repository.
2. Install required Python packages.

3. Ensure FFmpeg and Vosk models are correctly set up in the `tools/` directory.


------

## 🚀 Usage

1. Run the main pipeline:

   ```bash
   python main.py
   ```

   Follow the prompts to select a video file, and the script will automatically extract audio, perform speech-to-text, and generate subtitles in the `output/` directory.

2. Supported subtitle format: `.srt`

------

## 📁 File Structure

```
realtime_subtitle/
├── tools/                    # External tools and models (FFmpeg, Vosk)
├── temp/                     # Temporary audio files
├── output/                   # Generated subtitles
├── extract_audio.py          # Audio extraction module
├── speech_to_text.py         # Speech-to-text module
├── generate_subtitles.py     # Subtitle generation module
└── main.py                   # Main script for the full pipeline
```

------

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvement or find any issues, feel free to create a pull request or submit an issue.

------

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE.txt) file for details.

------

## 📞 Contact

If you have any questions, feel free to reach out at [astridstark25963@gmail.com](mailto:astridstark25963@gmail.com).
