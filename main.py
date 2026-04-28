import sys
import os
from pytubefix import innertube

from utils.console import clear_console, print_error, print_info, print_separator, print_success
from utils.ask import ask_audio_only, ask_video_or_playlist, get_url
from utils.video_dl import download_video
from utils.playlist_dl import download_playlist
from utils.file import get_main_script_location

# ------------------------------------------------------------------------------
# Application code here
def main():
    # --------------------------------------------------------------------------
    # Clear console
    clear_console()
    print_separator()
    # --------------------------------------------------------------------------
    # Get URL from user
    url = get_url()
    print_separator()
    # --------------------------------------------------------------------------
    # Check if url is video, playlist, or channel
    type = ask_video_or_playlist()
    print_separator()
    # --------------------------------------------------------------------------
    if type == "Video":
        audio_only = ask_audio_only()
        print_separator()
        download_video(url, audio_only)
    elif type == "Playlist":
        download_playlist(url)
    else:
        print_error("Choice")
        
    print_separator()
    # --------------------------------------------------------------------------

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        # ----------------------------------------------------------------------
        # Overwrite PyTube's default cache directory to keep user's OAuth info in package mode
        # Link: https://github.com/pytube/pytube/issues/1322
        
        # app_path is the directory the cache folder will be created in
        innertube._cache_dir = os.path.join(get_main_script_location(), "__cache__") # ./__cache__
        innertube._token_file = os.path.join(innertube._cache_dir, 'tokens.json')
        # ----------------------------------------------------------------------
        # Run the app
        main()
        # ----------------------------------------------------------------------
    except Exception as e:
        print_separator()
        print_error(f"An error occurred: {e}")
        print_info("Press Enter to exit...")
        input()  # Wait for the user to press Enter
        print_separator()
        sys.exit(1)
    else:
        print_separator()
        print_success("Done")
        print_info("Press Enter to exit...")
        input()  # Wait for the user to press Enter
        print_separator()
        sys.exit(0)