import re
import os
import shutil
import inquirer
from simple_chalk import chalk
from pytubefix import Stream, YouTube

from .file import slugify

from .console import print_error

# ------------------------------------------------------------------------------
# Get YouTube URL from user
def get_url():
    questions = [
        inquirer.Text('url', 
                        message=chalk.blue.bold("Please enter a YouTube URL"), 
                        validate=lambda _, x: re.match(r'https?://(?:www\.)?youtube\.com/.*', x)
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
# Check if url is video, playlist, or channel
def check_url(url):
    questions = [
    inquirer.List('type',
                    message=chalk.blue.bold("Is this a video, playlist, or channel?"),
                    choices=['Video', 'Playlist', 'Channel'],
                ),
    ]
    answers = inquirer.prompt(questions)

    return answers['type']
    
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
        return f"{stream.itag}: {stream.resolution} - {stream.filesize_mb}MB - ({stream.mime_type}) - ({codec})"
    
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
                        default="./out",
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
    
    # If dir exists, ask user whether to remove it
    if os.path.exists(dir):
        # Ask user whether to remove it
        remove_file = ask_yes_no(f"File {dir} already exists. Do you want to remove it?")
        if remove_file:
            shutil.rmtree(dir)
        else:
            # Recursively ask for filename
            return get_filename(default_dir)

    return dir

# ------------------------------------------------------------------------------
