# 🎙️ SRT to TTS Sync

This project converts **SRT subtitle files** into a fully synchronized **voice-over audio track** using [Edge TTS](https://github.com/rany2/edge-tts) and [pydub](https://github.com/jiaaro/pydub). Each subtitle line is processed into an audio clip, aligned with its timestamp, and stitched together into a single MP3 file that matches your video timing.

## ✨ Features

* Parse `.srt` subtitle files into structured text + timestamps
* Generate **natural TTS audio** with customizable **voice, pitch, and speed**
* Auto-align narration with subtitle timing (silences inserted where needed)
* Export a single **synchronized MP3 file**
* Temporary files cleaned up automatically

## 📂 Project Structure

```
.
├── input2.srt         # Your subtitle file
├── output_synced2.mp3 # Final generated audio
├── temp_audio/        # Temporary clips (auto-deleted)
└── main.py            # The main script
```

## 🚀 Usage

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   (Make sure `ffmpeg` is installed for `pydub` to work.)

2. Place your subtitles in `input.srt`.

3. Run the script:

   ```bash
   python main.py
   ```

4. Get your synchronized narration in `output_synced.mp3`.

## ⚙️ Configuration

You can customize in `main.py`:

* `VOICE` → Select a different Edge TTS voice (e.g. `en-US-BrianMultilingualNeural`)
* `RATE` → Control speaking speed (e.g. `-1%`, `+10%`)
* `PITCH` → Adjust pitch (e.g. `-5Hz`, `+2Hz`)
* `OUTPUT_FILE` → Change the name of the generated MP3

## 🛠️ Requirements

* Python 3.8+
* [edge-tts](https://github.com/rany2/edge-tts)
* [pydub](https://github.com/jiaaro/pydub)
* [tqdm](https://github.com/tqdm/tqdm)
* [ffmpeg](https://ffmpeg.org/) installed and in PATH

## 🎯 Example

If your `input.srt` contains:

```
1
00:00:00,000 --> 00:00:03,000
Hello, welcome to the tutorial!

2
00:00:05,000 --> 00:00:07,000
Let's get started.
```

The script generates an MP3 that speaks each line at the correct time, with silence automatically inserted between subtitles.

---

✅ Perfect for creating **tutorial narrations, video dubs, or accessibility audio** directly from subtitles.
