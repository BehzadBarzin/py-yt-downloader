import os
import requests
from pytubefix import YouTube
from prompt_toolkit import prompt
import sys
from tqdm import tqdm
from moviepy.editor import VideoFileClip, AudioFileClip

# -------------------------------------------------------------------------------------------------------
# Clear console
os.system("cls" if os.name == "nt" else "clear")
# -------------------------------------------------------------------------------------------------------

# Function to get public IP
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json().get("ip")
    except requests.RequestException as e:
        print("Error fetching public IP:", e)
        return None

# Check if the current IP is from Iran
ip = get_public_ip()

if ip:
    response = requests.get(f'https://ipapi.co/{ip}/json/').json()
    country = response.get("country_name")
    if country == "Iran":
        print("❌You are in Iran! Please, connect to VPN.")
        sys.exit(1)
    else:
        print(f"✅You are in {country}")
else:
    print("❌Could not determine IP location.")
    sys.exit(1)

print('-' * 30)

# -------------------------------------------------------------------------------------------------------
# Get URL from user
while True:
    url = prompt("❔Please enter a YouTube URL: ")
    try:
        # oauth options prompt user to login to YouTube
        video = YouTube(url, use_oauth=True, allow_oauth_cache=True)
                
        # Read this: https://github.com/JuanBindez/pytubefix/pull/209
        # video = YouTube(url, use_po_token=True)
        break
    except Exception as e:
        print("❌Invalid YouTube URL. Please try again.")

print('-' * 30)

# -------------------------------------------------------------------------------------------------------
# Filter formats with both audio and video
formats = [
    stream for stream in video.streams.filter(is_dash=True)
]

# # Ask user whether to show only mp4 formats
# mp4_only = prompt("❔Show only mp4 formats? (yes/no) [default: no]: ").lower()
# if mp4_only in ("yes", "y"):
#     formats = [stream for stream in formats if stream.mime_type == "video/mp4"]

# Parse formats for display
parsed_formats = {str(stream.itag): stream for stream in formats}

# -------------------------------------------------------------------------------------------------------
'''
YouTube typically splits high-quality video and audio into separate streams, which is why some streams only contain video and others only contain audio.

- Progressive streams (lower-quality, usually up to 720p) contain both video and audio, which is why formats like 18 (360p) include both.
    + filter streams by: [stream for stream in video.streams.filter(progressive=True)]
- DASH (Dynamic Adaptive Streaming over HTTP) streams (higher resolutions) split video and audio into separate streams to optimize quality and allow streaming of different qualities. For example:
    + filter streams by: [stream for stream in video.streams.filter(is_dash=True)]
'''
# -------------------------------------------------------------------------------------------------------
# Separate audio-only and video-only streams
video_formats = [stream for stream in formats if stream.includes_video_track and not stream.includes_audio_track]
audio_formats = [stream for stream in formats if stream.includes_audio_track and not stream.includes_video_track]

# Display video formats
print("📼 Available video-only formats:")
for stream in video_formats:
    print(f"> {stream.itag}: {stream.resolution} ({stream.mime_type}) (Video Codec: {stream.video_codec})")

# Let the user select the desired video stream
video_itag = prompt("❔Enter the itag of the video format you want: ")

print('-' * 30)

# Display audio formats
print("🔉 Available audio-only formats:")
for stream in audio_formats:
    print(f"> {stream.itag}: {stream.abr} ({stream.mime_type}) (Audio Codec: {stream.audio_codec})")

# Let the user select the desired audio stream
audio_itag = prompt("❔Enter the itag of the audio format you want: ")

print('-' * 30)

# Retrieve the selected streams
selected_video_format = parsed_formats.get(video_itag)
selected_audio_format = parsed_formats.get(audio_itag)

if not selected_video_format or not selected_audio_format:
    print("❌Invalid selection.")
    sys.exit(1)

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
# Ask user for filename
default_file_name = video.title
user_file_name = prompt(f"❔Please enter a file name [default: {default_file_name}]: ")

file_dir = "./"
file_name = f"{user_file_name or default_file_name}.{selected_video_format.subtype}"
# Temp files to store video and audio streams separately
file_name_video = f"{file_name}_video"
file_name_audio = f"{file_name}_audio"

file_path = os.path.join(file_dir, file_name)

# If file exists, ask user whether to remove it
if os.path.exists(file_path):
    remove_file = prompt(f"❔File {file_path} already exists. Do you want to remove it? (yes/no) [default: no]: ").lower()
    if remove_file in ("yes", "y"):
        os.remove(file_path)
    else:
        print(f"❌File {file_path} already exists.")
        sys.exit(1)

print('-' * 30)

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
# Helper function to download a stream and show progress
def download(stream, file_dir, file_name):
    progress_bar = tqdm(total=stream.filesize, unit="B", unit_scale=True, desc="Downloading Stream")
    # Define progress callback functions
    def progress_cb(stream, chunk, bytes_remaining):
        bytes_downloaded = stream.filesize - bytes_remaining
        progress_bar.n = bytes_downloaded
        progress_bar.refresh()
    
    # Register progress callbacks
    video.register_on_progress_callback(progress_cb)
    # Download the stream
    stream.download(output_path=file_dir, filename=file_name)
    progress_bar.close()
    
    print('-' * 30)
    
# -------------------------------------------------------------------------------------------------------
# Download video and audio streams
video_path = os.path.join(file_dir, file_name_video)
audio_path = os.path.join(file_dir, file_name_audio)

try:
    # Download video stream
    download(selected_video_format, file_dir, file_name_video)
    
    # Download audio stream
    download(selected_audio_format, file_dir, file_name_audio)

    # Merge video and audio using ffmpeg-python and imageio-ffmpeg
    print("🔄 Merging audio and video...")
    # Load the video file
    video_clip = VideoFileClip(video_path)
    # Load the audio file
    audio_clip = AudioFileClip(audio_path)
    # Set the audio of the video
    video_clip = video_clip.set_audio(audio_clip)
    # Write the result to a file
    video_clip.write_videofile(file_path)
    # Close files
    video_clip.close()
    audio_clip.close()
    print(f"✅ Merged video saved to {file_path}")

except Exception as e:
    print("❌Error during download or merge:", e)
    sys.exit(1)
finally:
    # Clean up temporary files
    if os.path.exists(video_path):
        os.remove(video_path)
    if os.path.exists(audio_path):
        os.remove(audio_path)