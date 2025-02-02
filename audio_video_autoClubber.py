#!/usr/bin/env python3
# clubber.py version 1.0.0
# Date: 2025-02-02 00:00:00 JST (example)
#
# This script pairs video files from the "inputvideo" folder with audio files from the
# "inputaudio" folder in sorted order. For each pair, it overlays the audio onto the video.
# If the audio is longer than the video, it will be trimmed to match the video's duration.
#
# Requirements:
# - ffmpeg must be installed and accessible via the command line.
#
# Usage:
#   Place your mp4 files in "inputvideo" and your mp3/wav files in "inputaudio". Run this script.
#   The output will be saved in the "output" folder with the same filename as the video.
#

import os
import subprocess
from datetime import datetime, timedelta, timezone

def get_jst_time():
    """Return the current date and time in JST."""
    jst = timezone(timedelta(hours=9))
    return datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S JST")

# Define folder paths
input_audio_folder = "inputaudio"
input_video_folder = "inputvideo"
output_folder = "output"

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# List and sort audio and video files
audio_files = sorted(
    [f for f in os.listdir(input_audio_folder) if f.lower().endswith((".mp3", ".wav"))]
)
video_files = sorted(
    [f for f in os.listdir(input_video_folder) if f.lower().endswith(".mp4")]
)

# Zip together the video and audio files in order
pairs = zip(video_files, audio_files)

for idx, (video_file, audio_file) in enumerate(pairs, start=1):
    video_path = os.path.join(input_video_folder, video_file)
    audio_path = os.path.join(input_audio_folder, audio_file)
    output_path = os.path.join(output_folder, video_file)  # Using video filename for output

    # Build the ffmpeg command:
    # - "-c:v copy" copies the video stream without re-encoding.
    # - "-c:a aac" encodes the audio to AAC format.
    # - "-shortest" trims the longer stream (audio, if it is longer) to the duration of the shorter (video).
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]

    print(f"[{get_jst_time()}] Processing ({idx}): '{video_file}' with audio '{audio_file}'")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[{get_jst_time()}] Error processing {video_file} with {audio_file}: {e}")

print(f"[{get_jst_time()}] Processing completed.")
