from utils.check_vpn import check_vpn
from utils.console import clear_console, print_error, print_separator
from utils.ask import check_url, get_url
from utils.video_dl import download_video
from utils.playlist_dl import download_playlist

# ------------------------------------------------------------------------------
# # Clear console
clear_console()
print_separator()
# ------------------------------------------------------------------------------
# # Check VPN
check_vpn()
print_separator()
# ------------------------------------------------------------------------------
# # Get URL from user
url = get_url()
print_separator()
# ------------------------------------------------------------------------------
# Check if url is video, playlist, or channel
type = check_url(url)
print_separator()
# ------------------------------------------------------------------------------
if type == "Video":
    download_video(url)
elif type == "Playlist":
    download_playlist(url)
else:
    print_error("Choice")
    
print_separator()
# ------------------------------------------------------------------------------

