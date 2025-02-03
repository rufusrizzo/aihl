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

# Copyright (C) 2023 Your Name

# Additional note:
# If you're distributing this software, you must include the full text of the GPLv3 
# license either in the source code or in a separate file named LICENSE or COPYING.
#Original author RileyC started on 2/3/2025

import whisper
import torch
import json
import sys
from paho.mqtt import client as mqtt_client

# Function to connect to MQTT broker
def connect_mqtt(broker, port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# Check if a config file path is provided
if len(sys.argv) < 2:
    print("Usage: ailogger-publish_text.py <CONFIG_FILE>")
    sys.exit(1)

config_file_path = sys.argv[1]

# Load configuration from file
try:
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print(f"Config file '{config_file_path}' not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Config file '{config_file_path}' is not valid JSON.")
    sys.exit(1)

# MQTT setup
mqtt_client = connect_mqtt(config['broker'], config['port'])
mqtt_topic = config['mqtt_topic']

# Check for available backend
if torch.backends.mps.is_available():  # macOS Metal backend
    device = "mps"
elif torch.cuda.is_available():  # CUDA (NVIDIA or ROCm for AMD)
    try:
        if torch.cuda.is_built():
            print(f"CUDA device: {torch.cuda.get_device_name(0)}")
            device = "cuda"
        elif torch.cuda.is_available():
            print(f"ROCm device: {torch.cuda.get_device_name(0)}")
            device = "cuda"
        else:
            device = "cpu"
    except Exception as e:
        print(f"Error detecting device: {e}")
        device = "cpu"
else:
    device = "cpu"

print(f"Using device: {device}")

# Load the Whisper model
model = whisper.load_model("base").to(device)

# Process each WAV file listed in the config
for wav_file in config['wav_files']:
    # Transcribe audio
    result = model.transcribe(wav_file)
    print(f"Transcription for {wav_file}: {result['text']}")
    
    # Publish to MQTT
    mqtt_client.publish(mqtt_topic, result['text'])

# Ensure all messages are sent before exiting
mqtt_client.loop_stop()

print("All WAV files processed. Exiting script.")
sys.exit(0)

