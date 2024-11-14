import sys
from utils.check_vpn import check_vpn
from utils.console import clear_console, print_error, print_info, print_separator, print_success
from utils.ask import check_url, get_url
from utils.video_dl import download_video
from utils.playlist_dl import download_playlist

# ------------------------------------------------------------------------------
# Application code here
def main():
    # --------------------------------------------------------------------------
    # Clear console
    clear_console()
    print_separator()
    # --------------------------------------------------------------------------
    # Check VPN
    check_vpn()
    print_separator()
    # --------------------------------------------------------------------------
    # Get URL from user
    url = get_url()
    print_separator()
    # --------------------------------------------------------------------------
    # Check if url is video, playlist, or channel
    type = check_url(url)
    print_separator()
    # --------------------------------------------------------------------------
    if type == "Video":
        download_video(url)
    elif type == "Playlist":
        download_playlist(url)
    else:
        print_error("Choice")
        
    print_separator()
    # --------------------------------------------------------------------------

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_separator()
        print_error(f"An error occurred: {e}")
        print_info("Press Enter to exit...")
        input()  # Wait for the user to clpress Enter
        print_separator()
        sys.exit(1)
    else:
        print_separator()
        print_success("Done")
        print_info("Press Enter to exit...")
        input()  # Wait for the user to press Enter
        print_separator()
        sys.exit(0)