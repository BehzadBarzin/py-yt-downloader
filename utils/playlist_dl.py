import os
import glob
from uuid import uuid4 as UUID
from pytubefix import Playlist, YouTube, Stream

from .ask import choose_format, get_dirname, resolutions, get_min_resolution, bitrates, get_min_bitrate
from .file import get_main_script_location, get_project_root, slugify
from .console import print_separator, print_error, print_success, print_info
from .video_dl import download, merge_audio_video

def download_playlist(url):
    # --------------------------------------------------------------------------
    # Initialize PyTube object with OAuth
    yt = Playlist(url, use_oauth=True, allow_oauth_cache=True)
    # --------------------------------------------------------------------------
    # Let user choose format (used to filter both with video and audio)
    format = choose_format() # "webm" or "mp4"
    print_separator()
    # --------------------------------------------------------------------------
    # Let user choose the directory name
    default_dir = os.path.join(get_main_script_location(), "videos",slugify(yt.title)) # Use playlist title (slug) as default directory
    file_dir = get_dirname(default_dir)
    print_separator()
    # --------------------------------------------------------------------------
    # Let user choose preferred video resolutions (e.g. "1080p")
    min_resolution = get_min_resolution()
    print_separator()
    print_info(f"We will only download {format} streams with minimum quality of {min_resolution} for video.")
    print_separator()
    # --------------------------------------------------------------------------
    # Let user choose preferred audio bitrate (e.g. "128kbps")
    min_bitrate = get_min_bitrate()
    print_separator()
    print_info(f"We will only download audio streams with minimum bitrate of {min_bitrate} for audio.")
    print_separator()
    # --------------------------------------------------------------------------
    # Download each video
    for idx, video in enumerate(yt.videos):
        print_info(f"Downloading video {idx + 1}/{len(yt.videos)}: {video.title}")
        download_video(video, file_dir, format, min_resolution, min_bitrate, idx + 1)
        print_separator()
    # --------------------------------------------------------------------------
    print_success("Playlist Downloaded")
    # --------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def download_video(yt: YouTube, file_dir: str, format: str, min_resolution: str, min_bitrate: str, playlist_idx: int):
    # --------------------------------------------------------------------------
    # Choose video stream
    all_video_stream: list[Stream] = [
        stream for stream in yt.streams.filter(is_dash=True).order_by("resolution").desc() if stream.includes_video_track and not stream.includes_audio_track
    ]

    # Filter streams that match the selected format
    all_video_stream = [stream for stream in all_video_stream if format in stream.mime_type]

    # Start from the minimum selected resolution, and find the highest quality video stream
    
    # A list of possible resolutions including and lower than what user selected
    video_stream = None
    lower_resolutions: list[str] = resolutions[resolutions.index(min_resolution):]
    for res in lower_resolutions:
        for stream in all_video_stream:
            if stream.resolution == res:
                video_stream = stream
                break
        # Break if video stream has been found
        if video_stream is not None:
            break
    if video_stream is None:
        print_error(f"No video stream available with minimum resolution of {min_resolution} or lower and format of {format}.")
        return
    # --------------------------------------------------------------------------
    # Get highest available audio stream
    all_audio_stream: list[Stream] = [
        stream for stream in yt.streams.filter(is_dash=True).order_by("abr").desc() if stream.includes_audio_track and not stream.includes_video_track
    ]
    
    # Filter streams that match the selected format
    all_audio_stream = [stream for stream in all_audio_stream if format in stream.mime_type]
    
    # Start from the minimum selected bitrate, and find the highest bitrate audio stream
    
    # A list of possible bitrates including and lower than what user selected
    audio_stream = None
    lower_bitrates: list[str] = bitrates[bitrates.index(min_bitrate):]
    for br in lower_bitrates:
        for stream in all_audio_stream:
            if stream.abr == br:
                audio_stream = stream
                break
        # Break if audio stream has been found
        if audio_stream is not None:
            break
    if audio_stream is None:
        print_error(f"No audio stream available with minimum bitrate of {min_bitrate} or lower and format of {format}.")
        return
    # --------------------------------------------------------------------------
    # Select file name that includes index in playlist
    file_slug = slugify(yt.title) # Used to see if file exists
    file_name = f"{playlist_idx}-{file_slug}.{video_stream.subtype}"
    # --------------------------------------------------------------------------
    # Define file names
    file_path = os.path.join(file_dir, file_name)
    
    # Select temp file names for video and audio streams
    random_id = str(UUID())[:8]
    video_file_name = f"temp_vid_{random_id}"

    audio_file_name = f"temp_aud_{random_id}"
    # --------------------------------------------------------------------------
    # If file exists, skip
    # Check to see if file exists by using a wildcard (*) in place of its idx and extension because file order and/or type might have changed
    found_files = glob.glob(os.path.join(file_dir, f"*{file_slug}*"))
    if len(found_files) > 0:
        print_info(f"Video \"{yt.title}\" already exists. Skipping...")
        return
    else:
        print_info(f"Downloading video: {file_name}")
    # --------------------------------------------------------------------------
    # Start download process and merge audio and video
    try:
        # ----------------------------------------------------------------------
        # Download video and audio streams
        downloaded_video_path = download(yt, video_stream, file_dir, video_file_name)
        downloaded_audio_path = download(yt, audio_stream, file_dir, audio_file_name)
        # ----------------------------------------------------------------------
        print_info("Download complete. Merging audio and video...")
        # ----------------------------------------------------------------------
        # Merge video and audio using ffmpeg-python
        merge_audio_video(downloaded_video_path, downloaded_audio_path, file_path)
        # ----------------------------------------------------------------------
    except Exception as e:
        print_error(f"Error during download or merge: {e}")
        exit(1)
    finally:
        # Clean up temporary files
        if os.path.exists(downloaded_video_path):
            os.remove(downloaded_video_path)
        if os.path.exists(downloaded_audio_path):
            os.remove(downloaded_audio_path)
        print_success("Video Downloaded")
    # --------------------------------------------------------------------------
