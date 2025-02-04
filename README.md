# AIHL (AI Ham Logger) Audio Transcription System

The inspiration for this project was POTA logging, Hurricane Helene (2024) after action, and the bike rides our Ham club VARA helps with.  The long term goal is the create a HW box that you connect your radio to and it breaks out audio to a computer with two or more Audio capture cards, and you can still use your radio normally.  The computer will transcribe the audio transmitted and received then output text to  several places to see and have for later.
This project involves a set of Python scripts to record audio, process it, transcribe the speech to text using Whisper, and publish the transcriptions to an MQTT broker. The system is designed to handle continuous recording and transcription, while managing the stored WAV files.

# Project Checklist

## Software

- [x] **Record Audio**
  - [x] Implement functionality to record audio in 30-second chunks.
  - [x] Store audio in WAV files.
  
- [ ] **Transcribe Audio to Text**
  - [x] Integrate Whisper model for transcribing audio to text.
  - [ ] Better GPU integration and testing
  - [ ] Document, or link setting up GPU configuration
  
  - [x] Set up MQTT communication for publishing transcribed text.
  - [x] Publish transcriptions to a specified MQTT topic.
  - [x] Log each transcription to a local file for record-keeping.

- [ ] **Create Webpage with Text Bubbles like IM/SMS**
  - [ ] Design and implement a webpage to display transcribed text in a conversational format (IM/SMS style).
  - [ ] Allow selecting which audio streams to display on the webpage.
  
- [ ] **Configuration Script with Audio Device to "Stream" Mapping**
  - [ ] Create a script for configuring which audio devices are mapped to specific streams.
  
- [ ] **Startup and Run Instructions**
  - [ ] Write comprehensive instructions for setting up and running the entire system.

---

## Hardware

- [ ] **Long-Term Goal: Create a PCB and Case for 2, 4, or 8 Inputs**
  - [ ] Design a custom PCB for audio input handling (2, 4, or 8 inputs).
  - [ ] Design and prototype a protective case for the system.
  
- [ ] **Modular Connectors for Different Radios**
  - [ ] Plan and implement modular connectors to support different radio setups.
  - [ ] Ensure flexibility for connecting various types of radios in the future.


## Overview

- **Audio Recording**: Records audio from a specified device in 30-second chunks.
- **Transcription**: The recorded audio is transcribed into text using the Whisper model.
- **Publishing**: The transcribed text, along with a timestamp (in local time and UTC), is published to an MQTT broker.
- **File Management**: Old WAV files are deleted when the specified maximum number of files is exceeded.

## Requirements

- Python 3.6 or higher
- Required libraries: `whisper`, `torch`, `paho-mqtt`, `pydub`, `sounddevice`, `pyaudio`, `pytz`
- Running a local MQTT broker (or specify the broker in the config file)

### Install Dependencies

```bash
pip install -r requirements.txt
Scripts
1. aihl-publish_text.py
This script takes a configuration file and a WAV file, transcribes the audio, and publishes the transcription along with a timestamp to an MQTT broker.

Usage
bash
python3 aihl-publish_text.py <CONFIG_FILE> <WAV_FILE>
<CONFIG_FILE>: Path to the JSON configuration file.
<WAV_FILE>: Path to the WAV file containing the recorded audio.
Example
bash

python3 aihl-publish_text.py conf/aihl.json capture_files/one/recording_20250203-103045.wav
This script transcribes the audio from the WAV file and publishes the transcription to the MQTT topic specified in the config file. It also logs the transcription to a log file.

2. aihl-record.py
This script continuously records audio in 30-second chunks, processes each recording, and manages the stored files.

Usage
bash
python3 aihl-record.py <CONFIG_FILE>
<CONFIG_FILE>: Path to the JSON configuration file.
Example
bash

python3 aihl-record.py conf/aihl.json
This script records audio, transcribes it using aihl-publish_text.py, and manages the storage of WAV files. It will keep the latest max_files number of files in the specified directory and delete the oldest files as needed.

3. list_audio_devices.py
This script lists the available audio input/output devices on your system.

Usage
bash
python3 list_audio_devices.py
This script will print all available audio devices along with their properties.

Configuration File (aihl.json)
The configuration file is a JSON file that specifies the parameters for the recording, transcription, and MQTT publishing.

Example aihl.json
json
{
    "broker": "localhost",
    "port": 1883,
    "mqtt_topic": "ailogger/transcription",
    "stream_number": 1,
    "audio_device": 4,
    "wav_directory": "./capture_files/one",
    "max_files": 10,
    "local_offset": -300,  
    "debug": true,
    "log_file": "./logs/ch1-transcription.log",
    "sample_wav_file": "./wav-samples/female.wav"
}
Configuration Fields
broker: The hostname or IP address of the MQTT broker.
port: The port number of the MQTT broker.
mqtt_topic: The topic to which transcriptions will be published.
stream_number: An identifier for the stream.
audio_device: The ID of the audio input device (use list_audio_devices.py to find available devices).
wav_directory: Directory to store the recorded WAV files.
max_files: The maximum number of WAV files to store before old ones are deleted.
local_offset: The offset (in minutes) to adjust local time (e.g., -300 for EST).
debug: If true, enables debug mode which uses a sample WAV file instead of recording.
log_file: The path to the log file where transcriptions will be saved.
sample_wav_file: Path to a sample WAV file for debug mode.
License
This project is licensed under the GNU General Public License v3.0. You can redistribute and modify it under the terms of the license.

Authors
Riley Chandler KF4EMZ (Original author)
Acknowledgements
Whisper model by OpenAI for speech recognition.
MQTT protocol for message publishing.
PyAudio, SoundDevice, and other libraries for audio recording.
