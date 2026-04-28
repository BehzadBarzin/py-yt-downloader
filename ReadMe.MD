# Youtube Downloader


## Project Setup (First time)
If you’re starting fresh, ensure `uv` is installed:
```bash
pip install uv
```

Then initialize a project:

```bash
uv init py-yt-downloader
cd py-yt-downloader
```

This automatically creates:

 - `pyproject.toml` (project definition)

 - `.python-version` (pinned Python version)

 - `uv.lock` (lockfile for reproducible installs)

### Install Dependencies

#### FFMPEG
Download FFMPEG from [this link](https://www.gyan.dev/ffmpeg/builds/) and copy `ffmpeg.exe` from the archive to `<project_root>/data`

#### Python Dependencies
```bash
# Option 1: Official pytube
uv add pytube

# Option 2: pytube with some fixes
uv add pytubefix

# Other libraries
uv add requests tqdm inquirer simple_chalk uuid
```
 - `pytube`: YouTube video downloader
    - `pytubefix`: If errors like HTTP 400 (or other issues) occur, use this instead of `pytube`
 - `requests`: Make HTTP calls
 - `tqdm`: Display progress bar in the terminal
 - `inquirer`: Ask user for inputs in the terminal
 - `simple_chalk`: Display colored text in the terminal
 - `uuid`: Generate UUID


 ## 🔥Subsequent Installations
 ```bash
 uv sync
 ```


 ## Run the app

```bash
uv run python .\main.py
```

 ## Package the app

 ### Install Dependencies
 ```bash
 uv add pyinstaller
 ```

 ### Run
Create the Executable with PyInstaller: Run the following command:

```bash
uv run pyinstaller --name "yt-dl" --add-data "data/*:data" --recursive-copy-metadata "inquirer" main.py
```
Options:
 - `--name`: Specify the name of the bundle.
 - `--add-data "<path-to-files>:<path-to-files-in-bundle>"`: Additional files or folders to include in the bundle. Replace `<path-to-files>` with the actual path to the asset files. Separate multiple files with a semicolon `;` on Windows and a colon `:` on macOS/Linux.
 - `--recursive-copy-metadata "inquirer"`: Some libraries need their metadata to be included in the bundle like this.