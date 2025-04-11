USAGE
This document explains how to run aihl.py and aihl-publish_text.py, two scripts that work together to record audio, transcribe it, and publish the results via MQTT.
Configuration
Both scripts require a config.json file in the project directory. Example:
json

{
    "audio_device": 2,
    "wav_directory": "./recordings",
    "max_files": 10,
    "broker": "192.168.1.10",
    "port": 1883,
    "mqtt_topic": "audio/transcriptions",
    "local_offset": -240,
    "log_file": "transcription.log",
    "debug": false,
    "sample_wav_file": "sample.wav"
}

Adjust audio_device, broker, port, and other fields as needed.

Running aihl.py
Purpose
Records 30-second audio clips continuously, saves them as WAV files, processes them with aihl-publish_text.py, and limits the number of stored files.
Command
bash

./aihl.py config.json

Example Output

Recording ./recordings/recording_20250409-143022.wav...
Saved ./recordings/recording_20250409-143022.wav
Running: python3 aihl-publish_text.py config.json ./recordings/recording_20250409-143022.wav

Runs indefinitely until stopped with Ctrl+C.

Running aihl-publish_text.py
Purpose
Transcribes a WAV file, timestamps the text, publishes it to an MQTT topic, and logs it to a file.
Command
bash

./aihl-publish_text.py config.json <WAV_FILE>

Example
bash

./aihl-publish_text.py config.json ./recordings/recording_20250409-143022.wav

Example Output

Using device: cpu
Connected to MQTT Broker!
Published to MQTT topic 'audio/transcriptions': 04-09-2025, 14:30:22, 18:30:22 UTC - Hello, world
Logged transcription to transcription.log
Exiting script.

Debug Mode
Set "debug": true in config.json to use a sample WAV file:
bash

./aihl-publish_text.py config.json anyfile.wav

Full Workflow
Start your MQTT broker (e.g., Mosquitto).

Run:
bash

./aihl.py config.json

Optionally monitor MQTT:
bash

mosquitto_sub -h 192.168.1.10 -t audio/transcriptions

aihl.py records audio and triggers aihl-publish_text.py to transcribe and publish.


