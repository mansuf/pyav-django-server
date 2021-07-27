# [PyAV](https://github.com/PyAV-Org/PyAV) Django Server

Unsuitable for production.

Not available in PyPI.

## Usage

### Server

Start the server

```bash
export SECRET_KEY="Insert key here"
python3 manage.py runserver localhost:5000
```

### Client

```python
import requests
import youtube_dl

yt = youtube_dl.YoutubeDL({'format': 'best'})
info = yt.extract_info('https://www.youtube.com/watch?v=MkNeIUgNPQ8', download=False)

data = {'url': info['url']}

# pcm_s16le format
r = requests.get('http://localhost:5000/pcm', json=data, stream=True)

# ogg libopus format
r = requests.get('http://localhost:5000/opus', json=data, stream=True)

...

```