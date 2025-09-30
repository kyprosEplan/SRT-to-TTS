import asyncio
import re
from pathlib import Path
import edge_tts
from pydub import AudioSegment
from tqdm import tqdm
import os

# --- Configuration ---
# The name of your SRT file
SRT_FILE = "input2.srt"
# The name of the final audio file
OUTPUT_FILE = "output_synced2.mp3"
# The TTS voice you want to use
VOICE = "en-US-BrianMultilingualNeural"
# Optional: Adjust the speed and pitch
RATE = "-1%"
PITCH = "-5Hz"
# A folder to store temporary audio clips
TEMP_DIR = Path("temp_audio")

def parse_srt(srt_content: str):
    """Parses SRT content into a list of subtitle objects."""
    srt_pattern = re.compile(
        r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?:\n\n|$)',
        re.DOTALL
    )

    matches = srt_pattern.findall(srt_content)
    
    subtitles = []
    for match in matches:
        start_time_str, end_time_str, text = match[1], match[2], match[3]
        subtitles.append({
            'start_ms': srt_time_to_ms(start_time_str),
            'text': text.strip().replace('\n', ' ')
        })
    return subtitles

def srt_time_to_ms(time_str: str) -> int:
    """Converts an SRT time string to milliseconds."""
    h, m, s, ms = map(int, re.split('[:,]', time_str))
    return (h * 3600 + m * 60 + s) * 1000 + ms

async def generate_tts_for_clip(text: str, voice: str, rate: str, pitch: str, output_path: Path):
    """Generates a single TTS audio clip."""
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch)
    await communicate.save(str(output_path))

async def main():
    # Create a directory for temporary files
    TEMP_DIR.mkdir(exist_ok=True)
    
    # Read and parse the SRT file
    try:
        with open(SRT_FILE, 'r', encoding='utf-8') as f:
            srt_content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: The file '{SRT_FILE}' was not found. Please create it and add your SRT content.")
        return
        
    subtitles = parse_srt(srt_content)
    if not subtitles:
        print("❌ Error: Could not find any subtitles in '{SRT_FILE}'. Please check its format.")
        return
        
    # Generate TTS for each subtitle line
    print(f"🎤 Generating {len(subtitles)} audio clips...")
    tasks = []
    for i, sub in enumerate(subtitles):
        clip_path = TEMP_DIR / f"clip_{i}.mp3"
        tasks.append(generate_tts_for_clip(sub['text'], VOICE, RATE, PITCH, clip_path))
    
    for future in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        await future

    # Stitch the audio clips together
    print("\n🪡 Stitching audio clips...")
    final_audio = AudioSegment.empty()
    last_position_ms = 0
    
    for i, sub in enumerate(tqdm(subtitles)):
        # Calculate silence duration
        silence_needed = sub['start_ms'] - last_position_ms
        if silence_needed > 0:
            final_audio += AudioSegment.silent(duration=silence_needed)
            
        # Add the audio clip
        clip_path = TEMP_DIR / f"clip_{i}.mp3"
        audio_clip = AudioSegment.from_mp3(clip_path)
        final_audio += audio_clip
        
        last_position_ms = len(final_audio)

    # Export the final combined audio
    print(f"\n💾 Exporting to '{OUTPUT_FILE}'...")
    final_audio.export(OUTPUT_FILE, format="mp3")
    
    # Clean up temporary files
    print("🧹 Cleaning up temporary files...")
    for i in range(len(subtitles)):
        os.remove(TEMP_DIR / f"clip_{i}.mp3")
    os.rmdir(TEMP_DIR)
    
    print("\n✅ Done! Your synchronized audio file is ready.")

if __name__ == "__main__":
    asyncio.run(main())