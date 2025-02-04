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

import whisper
import torch
import json
import sys
from paho.mqtt import client as mqtt_client
import os
import datetime
import pytz

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

# Get the formatted timestamp with local and UTC time
def get_timestamp(local_offset):
    # Get UTC time
    utc_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    
    # Apply local offset (in minutes)
    local_time = utc_time + datetime.timedelta(minutes=local_offset)
    
    # Format timestamps
    local_time_str = local_time.strftime('%m-%d-%Y, %H:%M:%S')
    utc_time_str = utc_time.strftime('%H:%M:%S UTC')
    
    # Full timestamp
    return f"{local_time_str}, {utc_time_str}"

# Ensure proper arguments are provided
if len(sys.argv) < 3:
    print("Usage: aihl-publish_text.py <CONFIG_FILE> <WAV_FILE>")
    sys.exit(1)

config_file_path = sys.argv[1]
wav_file = sys.argv[2]

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

# Check for debug flag and sample file in config
debug_mode = config.get('debug', False)
sample_wav_file = config.get('sample_wav_file', '')

if debug_mode:
    # Use sample WAV file if debug mode is enabled
    if not sample_wav_file or not os.path.isfile(sample_wav_file):
        print("Error: No valid sample WAV file specified in debug mode.")
        sys.exit(1)
    wav_file = sample_wav_file
    print(f"Debug mode enabled. Using sample WAV file: {wav_file}")

# Validate WAV file existence
if not os.path.isfile(wav_file):
    print(f"Error: WAV file '{wav_file}' not found.")
    sys.exit(1)

# MQTT setup
mqtt_client = connect_mqtt(config['broker'], config['port'])
mqtt_topic = config['mqtt_topic']

# Load local timezone offset from config
local_offset = config.get('local_offset', 0)  # Default to 0 if not set

# Check for log file in config
log_file = config.get('log_file', 'transcription.log')

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

# Transcribe audio
result = model.transcribe(wav_file)
transcribed_text = result['text'].strip()

# Check if there is any text to publish
if transcribed_text:
    # Get timestamp
    timestamp = get_timestamp(local_offset)
    
    # Create the message with timestamp
    message = f"{timestamp} - {transcribed_text}"
    
    # Publish to MQTT
    mqtt_client.publish(mqtt_topic, message)
    print(f"Published to MQTT topic '{mqtt_topic}': {message}")

    # Write to log file
    with open(log_file, 'a') as log:
        log.write(f"{timestamp} - {transcribed_text}\n")
    print(f"Logged transcription to {log_file}")

else:
    print("No transcription available, nothing to publish.")

# Ensure all messages are sent before exiting
mqtt_client.loop_stop()

print("Exiting script.")
sys.exit(0)

