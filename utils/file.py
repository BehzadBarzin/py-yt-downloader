import os
import sys
import unicodedata
import re

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


# ------------------------------------------------------------------------------
def get_project_root():
    """
    Returns the root directory of the project/package.
    
    - If running in a PyInstaller bundle, returns the temporary directory used by PyInstaller.
    - If running in a regular Python environment, traverses up from the main script's directory
    to find the root of the project.
    """
    if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
        return sys._MEIPASS
    else:
        # Running in a normal Python environment
        return os.path.dirname(os.path.abspath(sys.argv[0]))

# ------------------------------------------------------------------------------
def get_desktop_dir():
    return os.path.join(os.path.expanduser("~"), "Desktop")