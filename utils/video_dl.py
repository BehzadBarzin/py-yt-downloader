from pytubefix import YouTube, Stream
import os
from uuid import uuid4 as UUID
from tqdm import tqdm
import subprocess

from .file import get_project_root

from .console import print_separator, print_error, print_success, print_info
from .ask import choose_stream, get_filename


def download_video(url):
    # --------------------------------------------------------------------------
    # Initialize PyTube object with OAuth
    yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
    # --------------------------------------------------------------------------
    # Let user choose video stream
    video_stream_options: list[Stream]  = [stream for stream in yt.streams.filter(is_dash=True).order_by("resolution").desc() if stream.includes_video_track and not stream.includes_audio_track]
    video_stream = choose_stream(video_stream_options, is_video=True)
    print_separator()
    # --------------------------------------------------------------------------
    # Let user choose audio stream
    audio_stream_options: list[Stream]  = [stream for stream in yt.streams.filter(is_dash=True).order_by("abr").desc() if stream.includes_audio_track and not stream.includes_video_track]
    audio_stream = choose_stream(audio_stream_options, is_video=False)
    print_separator()
    # --------------------------------------------------------------------------
    # Let user choose the file and directory names
    (file_dir, file_name) = get_filename(yt, video_stream)
    file_path = os.path.join(file_dir, file_name)
    # Select temp file names for video and audio streams
    video_file_name = f"temp_vid_{UUID()}.{video_stream.subtype}"
    video_file_path = os.path.join(file_dir, video_file_name)
    
    audio_file_name = f"temp_aud_{UUID()}.{audio_stream.subtype}"
    audio_file_path = os.path.join(file_dir, audio_file_name)
    print_separator()
    # --------------------------------------------------------------------------
    # Start download process and merge audio and video
    try:
        # ----------------------------------------------------------------------
        # Download video and audio streams
        download(yt, video_stream, file_dir, video_file_name)
        download(yt, audio_stream, file_dir, audio_file_name)
        # ----------------------------------------------------------------------
        print_separator()
        print_info("Download complete. Merging audio and video...")
        # ----------------------------------------------------------------------
        # Merge video and audio using ffmpeg-python
        merge_audio_video(video_file_path, audio_file_path, file_path)
        # ----------------------------------------------------------------------
    except Exception as e:
        print_separator()
        print_error("Error during download or merge:", e)
        exit(1)
    finally:
        # Clean up temporary files
        if os.path.exists(video_file_path):
            os.remove(video_file_path)
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)
        print_separator()
        print_success("Done")
    # --------------------------------------------------------------------------
    

# ------------------------------------------------------------------------------
# Helper function to download a stream and show progress
def download(yt: YouTube, stream: Stream, file_dir: str, file_name: str):
    # Define progress bar
    progress_bar = tqdm(total=stream.filesize, unit="B", unit_scale=True, desc="Downloading Stream")
    
    # Define progress callback functions
    def progress_cb(stream, chunk, bytes_remaining):
        bytes_downloaded = stream.filesize - bytes_remaining
        progress_bar.n = bytes_downloaded
        progress_bar.refresh()
    
    # Register progress callbacks
    yt.register_on_progress_callback(progress_cb)
    
    # Download the stream
    stream.download(output_path=file_dir, filename=file_name)
    
    # Close progress bar
    progress_bar.close()

# ------------------------------------------------------------------------------
# Merge audio and video
def merge_audio_video(video_path, audio_path, output_path):
    # Path to ffmpeg executable
    ffmpeg_path = os.path.join(get_project_root(), "data", "ffmpeg.exe")
    
    # Command to merge video and audio while keeping original quality
    command = [
        ffmpeg_path,
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',    # Copy video codec to retain quality
        '-c:a', 'copy',    # Copy audio codec to retain quality
        output_path
    ]
    
    # Run the command
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print_success(f"Merged file saved to: {output_path}")

# ------------------------------------------------------------------------------
