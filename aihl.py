#!/home/riley/pvenv/bin/python3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Copyright (C) 2025 Riley Chandler

# Additional note:
# If you're distributing this software, you must include the full text of the GPLv3 
# license either in the source code or in a separate file named LICENSE or COPYING.
#Original author RileyC started on 2/3/2025

import os
import time
import wave
import json
import argparse
import subprocess
import sounddevice as sd
from collections import deque

def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

def record_audio(filename, device, duration=30, samplerate=44100, channels=1):
    print(f"Recording {filename}...")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype='int16', device=device)
    sd.wait()
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())
    print(f"Saved {filename}")

def process_audio(config_file, wav_file):
    cmd = ["python3", "aihl-publish_text.py", config_file, wav_file]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def manage_files(directory, max_files):
    files = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".wav")], key=os.path.getctime)
    while len(files) > max_files:
        oldest = files.pop(0)
        os.remove(oldest)
        print(f"Deleted old file: {oldest}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to configuration file")
    args = parser.parse_args()

    config = load_config(args.config)
    device = config.get("audio_device", None)
    directory = config.get("wav_directory", "./recordings")
    max_files = config.get("max_files", 10)
    os.makedirs(directory, exist_ok=True)

    file_queue = deque(maxlen=max_files)
    
    while True:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        wav_file = os.path.join(directory, f"recording_{timestamp}.wav")
        record_audio(wav_file, device)
        process_audio(args.config, wav_file)
        file_queue.append(wav_file)
        manage_files(directory, max_files)

if __name__ == "__main__":
    main()

