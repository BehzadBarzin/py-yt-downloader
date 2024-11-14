# Youtube Downloader


## Python Virtual Environment

### Setup Env
```bash
python -m venv .py-yt-downloader
```
- Note: Virtual environment path is ignored in the `.gitignore` file. If a new name is chosen, that value should be updated.

### Activate Env
```bash
.\.py-yt-downloader\Scripts\activate
```


## Install Dependencies

### GeoIP DB
Download the `GeoLite2-Country.mmdb` file from [this link](https://github.com/P3TERX/GeoLite.mmdb) and copy to `./utils/bin`

### FFMPEG
Download FFMPEG from [this link](https://www.gyan.dev/ffmpeg/builds/) and copy `ffmpeg.exe` from the archive to `./utils/bin`

### Python Dependencies
```bash
pip install pytubefix requests tqdm inquirer simple_chalk uuid geoip2
```
 - `pytubefix`: Fixed fork of `pytube` YouTube video downloader
    - `pytube` has been having some issues. For now, we would use `pytubefix` instead.
 - `requests`: Make HTTP calls
 - `tqdm`: Display progress bar in the terminal
 - `inquirer`: Ask user for inputs in the terminal
 - `simple_chalk`: Display colored text in the terminal
 - `uuid`: Generate UUID
 - `geoip2`: Uses the `GeoLite2-Country.mmdb` file to find the country for the an IP address.