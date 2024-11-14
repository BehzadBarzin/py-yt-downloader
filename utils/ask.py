import re
import os
import inquirer
from simple_chalk import chalk
from pytubefix import Stream, YouTube

from .file import get_desktop_dir, get_project_root, slugify

from .console import print_error

# ------------------------------------------------------------------------------
# Get YouTube URL from user
def get_url():
    questions = [
        inquirer.Text('url', 
                        message=chalk.blue.bold("Please enter a YouTube URL"), 
                        validate=lambda _, x: re.match(r'https?://(?:www\.|m\.)?youtube\.com/.*', x)
                    ),
    ]
    answers = inquirer.prompt(questions)

    return answers['url']

# ------------------------------------------------------------------------------
# Ask Yes/No question
def ask_yes_no(question):
    questions = [
        inquirer.List('yes_no',
                        message=chalk.blue.bold(question),
                        choices=['Yes', 'No'],
                        default='No',
                        carousel=True
                    ),
    ]
    answers = inquirer.prompt(questions)

    return True if answers['yes_no'] == 'Yes' else False

# ------------------------------------------------------------------------------
# Check if url is video or playlist
def check_url(url):
    questions = [
    inquirer.List('type',
                    message=chalk.blue.bold("Is this a video or playlist?"),
                    choices=['Video', 'Playlist'],
                ),
    ]
    answers = inquirer.prompt(questions)

    return answers['type']
    
# ------------------------------------------------------------------------------
# Choose format (webm/mp4)
def choose_format():
    questions = [
        inquirer.List('format',
                        message=chalk.blue.bold("Please select a format"),
                        choices=['webm', 'mp4'],
                        default='webm',
                    ),
    ]
    answers = inquirer.prompt(questions)

    return answers['format']

# ------------------------------------------------------------------------------
# Choose stream from list
def choose_stream(streams: list[Stream], is_video: bool):
    # Check if there are any streams
    if (len(streams) == 0):
        print_error(f"No streams available.")
        exit(1)
    
    # Create message based on stream type
    msg = "Please select a stream"
    if (is_video):
        msg = f"Please select a video stream"
    else:
        msg = f"Please select an audio stream"
    
    # Function to convert stream to string
    def stream_to_string(stream: Stream):
        codec = stream.video_codec if is_video else stream.audio_codec
        return f"{stream.itag}: {stream.resolution if is_video else stream.abr} - {stream.filesize_mb}MB - ({stream.mime_type}) - ({codec})"
    
    # Compile a list of string options from the streams
    options = [
        stream_to_string(stream) for stream in streams
    ]
    
    # Ask user to select a stream
    questions = [
            inquirer.List('stream',
                    message=chalk.blue.bold(msg),
                    choices=options,
            ),
    ]
    answers = inquirer.prompt(questions)

    # Get selected itag from selected string
    selected_itag = answers['stream'].split(":")[0]
    
    # Find the stream with the selected itag
    selected_stream = None
    for stream in streams:
        if (stream.itag == int(selected_itag)):
            selected_stream = stream
            break

    if selected_stream == None:
        print_error("Invalid selection.")
        exit(1)

    return selected_stream

# ------------------------------------------------------------------------------
# Ask user for filename
def get_filename(yt: YouTube, selected_video_stream: Stream):
    # This is a recursive function. if the file exists and user doesn't want to remove it, it asks for a new filename or directory.
    
    # Ask user for filename and directory
    questions = [
        inquirer.Path('file_name', 
                        message=chalk.blue.bold("Please enter a file name"), 
                        path_type=inquirer.Path.FILE,
                        default=slugify(yt.title),
                    ),
        inquirer.Path('file_dir',
                        message=chalk.blue.bold("Please enter a directory"),
                        path_type=inquirer.Path.DIRECTORY,
                        default=os.path.join(get_desktop_dir(), "yt-dl"),
                    ),
    ]
    
    answers = inquirer.prompt(questions)
    
    # Create full file path
    file_dir = answers['file_dir']
    file_name = f"{answers['file_name']}.{selected_video_stream.subtype}" # Add video file extension
    file_path = os.path.join(file_dir, file_name)
    
    # If file exists, ask user whether to remove it
    if os.path.exists(file_path):
        # Ask user whether to remove it
        remove_file = ask_yes_no(f"File {file_path} already exists. Do you want to remove it?")
        if remove_file:
            os.remove(file_path)
        else:
            # Recursively ask for filename
            return get_filename(yt, selected_video_stream)

    return (file_dir, file_name)
    

# ------------------------------------------------------------------------------
# Ask user for directory name
def get_dirname(default_dir: str):
    # This is a recursive function. if the file exists and user doesn't want to remove it, it asks for a new filename or directory.
    
    # Ask user for filename and directory
    questions = [
        inquirer.Path('dir',
                        message=chalk.blue.bold("Please enter a directory"),
                        path_type=inquirer.Path.DIRECTORY,
                        default=default_dir,
                    ),
    ]
    
    answers = inquirer.prompt(questions)
    
    dir = answers['dir']
    
    # If dir exists, ask user whether to update it
    if os.path.exists(dir):
        # Ask user whether to update it
        update_it = ask_yes_no(f"Directory {dir} already exists. Do you want to update it?")
        if update_it:
            # We just need to run the download playlist again it would automatically skip the existing videos
            return dir
        else:
            # Recursively ask for directory name
            return get_dirname(default_dir)

    return dir

# ------------------------------------------------------------------------------
# Ask user for preferred maximum resolution
resolutions = [
    '4320p', # 8K
    '2160p', # 4K
    '1440p', # 2K
    '1080p', # Full HD
    '720p',
    '480p',
    '360p',
    '240p',
    '144p',
]
    
def get_min_resolution(): 
    questions = [
        inquirer.List('min_resolution', 
                        message=chalk.blue.bold("Please select a minimum resolution (if it's not available, a lower resolution will be used)"), 
                        choices=resolutions,
                        default=resolutions[0]
                    ),
    ]
    answers = inquirer.prompt(questions)

    return answers['min_resolution']
# ------------------------------------------------------------------------------

bitrates = [
    '160kbps', 
    '128kbps', 
    '70kbps', 
    '50kbps', 
    '48kbps'
]
def get_min_bitrate():
    questions = [
        inquirer.List('min_bitrate', 
                        message=chalk.blue.bold("Please select a minimum bitrate (if it's not available, a lower bitrate will be used)"), 
                        choices=bitrates,
                        default=bitrates[0]
                    ),
    ]
    answers = inquirer.prompt(questions)

    return answers['min_bitrate']

# ------------------------------------------------------------------------------