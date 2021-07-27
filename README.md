# [PyAV](https://github.com/PyAV-Org/PyAV) Django Server

Unsuitable for production.

Not available in PyPI.

The server will take & convert audio only.

## Usage

### Server

Start the server

```bash
# For linux / MacOS
export SECRET_KEY="Insert key here"
# For windows
set SECRET_KEY="Insert key here"

python3 manage.py runserver localhost:5000
```

### Client

```python
import requests
import youtube_dl

yt = youtube_dl.YoutubeDL({'format': 'best'})
info = yt.extract_info('https://www.youtube.com/watch?v=MkNeIUgNPQ8', download=False)

# PCM Signed 16-bit 48000Hz
data = {
    'url': info['url'],
    'format': 's16le',
    'codec': 'pcm_s16le',
    'rate': 48000,
}

r = requests.get('http://localhost:5000', json=data, stream=True)

# Complete required json data
# Ogg libopus 48000Hz
data = {
    'url': info['url'],
    'format': 'ogg',
    'codec': 'libopus',
    'rate': 48000,
    'seek': 80 # Jump to 80 seconds from begin stream
}

r = requests.get('http://localhost:5000', json=data, stream=True)

...

```