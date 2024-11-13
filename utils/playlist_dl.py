from pytubefix import Playlist, Stream
from collections import defaultdict

from .ask import get_dirname, choose_stream
from .file import slugify
from .console import print_separator, print_error, print_success, print_info

def download_playlist(url):
    # --------------------------------------------------------------------------
    # Initialize PyTube object with OAuth
    yt = Playlist(url, use_oauth=True, allow_oauth_cache=True)
    # --------------------------------------------------------------------------    
    # Get streams that are shared across all videos
    (common_audio, common_video) = get_common_streams(yt)
    # --------------------------------------------------------------------------
    # Let user choose video stream
    video_stream = choose_stream(common_video, is_video=True)
    print_separator()
    # --------------------------------------------------------------------------
    # Let user choose audio stream
    audio_stream = choose_stream(common_audio, is_video=False)
    print_separator()
    # --------------------------------------------------------------------------
    # Let user choose the directory name
    default_dir = f"./{slugify(yt.title)}" # Use playlist title (slug) as default directory
    dir = get_dirname(default_dir)
    # --------------------------------------------------------------------------
    print(video_stream)
    print(audio_stream)
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Function to find common streams across all videos in the playlist
def get_common_streams(yt: Playlist):
    common_audio_streams = defaultdict(int)
    common_video_streams = defaultdict(int)
    
    # Initialize lists for common audio and video streams
    for video in yt.videos:
        # Get streams for the video
        audio_streams = [stream for stream in video.streams.filter(is_dash=True) if stream.includes_video_track and not stream.includes_audio_track]
        video_streams = [stream for stream in video.streams.filter(is_dash=True) if stream.includes_audio_track and not stream.includes_video_track]
        
        # Count each unique stream in all videos
        for stream in audio_streams:
            common_audio_streams[stream.itag] += 1
        
        for stream in video_streams:
            common_video_streams[stream.itag] += 1
    
    # Filter out streams that are not common to all videos
    total_videos = len(yt.video_urls)
    common_audio = [stream for stream, count in common_audio_streams.items() if count == total_videos]
    common_video = [stream for stream, count in common_video_streams.items() if count == total_videos]

    return common_audio, common_video