
# DeezSpot 🎵

A powerful Python library for downloading music from Deezer and Spotify. Clone of the original deezloader with additional features and improvements.

## ✨ Features

- Download songs, albums, playlists from Deezer
- Download songs, albums, playlists, episode from Spotify
- Support for multiple audio qualities (MP3, FLAC) and OGG for spotify
- Download podcast episodes
- Batch downloading
- Progress bar support
- ID3 tags and artwork

## 🚀 Installation

```bash
pip install deezspot
```

## 🔑 Authentication Setup

### Deezer Authentication
1. Get your Deezer ARL token from browser cookies after logging in to Deezer
2. Use the token in your code:
```python
from deezloader.deezloader import DeeLogin

dl = DeeLogin(arl='your_arl_token', email='', password='')
```

### Spotify Authentication
1. Clone the librespot-auth repository:
```bash
git clone https://github.com/dspearson/librespot-auth
cd librespot-auth
cargo build --release
```

2. Generate credentials:
```bash
./target/release/librespot-auth
```

3. Adjust your credentials.json with the format:
```json
{
    "username": "your_spotify_username",
    "credentials": "your_credentials_string",
    "type": "AUTHENTICATION_STORED_SPOTIFY_CREDENTIALS"
}
```

## 📚 Usage Examples

### Downloading with Deezer 
```python
from deezloader.deezloader import DeeLogin

dl = DeeLogin(arl='your_arl_token', email='', password='')

# Download single track
dl.download_trackdee(
    link_track='https://www.deezer.com/track/123456789',
    output_dir='./downloads',
    quality_download='MP3_320',
    recursive_quality=False,
    recursive_download=False
)

# Download album
dl.download_albumdee(
    link_album='https://www.deezer.com/album/123456789',
    output_dir='./downloads/albums',
    quality_download='FLAC',
    recursive_quality=True,
    recursive_download=False
)

# Download playlist
dl.download_playlistdee(
    link_playlist='https://www.deezer.com/playlist/123456789',
    output_dir='./downloads/playlists',
    quality_download='MP3_320',
    recursive_quality=True,
    recursive_download=False
)

# Download artist
dl.download_artistdee(
    link_artist='https://www.deezer.com/artist/123456789',
    output_dir='./downloads/artists',
    quality_download='MP3_320',
    recursive_quality=True,
    recursive_download=False
)
```

### Downloading with Spotify 
```python
import sys
import os
import traceback

# Add the local deezloader directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from deezloader.spotloader import SpoLogin

try:
    # Initialize Spotify client
    # Make sure to generate credentials.json using librespot-auth first
    credentials_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'credentials.json'))
    spo = SpoLogin(credentials_path=credentials_path)

    # Download single track
    track = spo.download_track(
        link_track="https://open.spotify.com/track/4tCtwWceOPWzenK2HAIJSb",
        output_dir="./downloads/tracks",
        quality_download="MP3_320",
        recursive_quality=False,
        recursive_download=False,
        not_interface=False,
        method_save=1
    )

    # Download album
    album = spo.download_album(
        link_album="https://open.spotify.com/album/6n4YU8iRm07O7lR1zQZypN",
        output_dir="./downloads/albums",
        quality_download="FLAC",
        recursive_quality=True,
        recursive_download=False,
        not_interface=False,
        method_save=1,
        make_zip=True
    )

    # Download playlist
    playlist = spo.download_playlist(
        link_playlist="https://open.spotify.com/playlist/1ZyEi4bBTYGTIlY23U1kwG",
        output_dir="./downloads/playlists",
        quality_download="MP3_320",
        recursive_quality=True,
        recursive_download=False,
        not_interface=False,
        method_save=1,
        make_zip=True
    )

    # Download episode
    episode = spo.download_episode(
        link_episode="https://open.spotify.com/episode/1hgO8Y3CCymyxn934lNtDq",
        output_dir="./downloads/episodes",
        quality_download="MP3_320",
        recursive_quality=False,
        recursive_download=False,
        not_interface=False,
        method_save=1
    )

except Exception as e:
    traceback.print_exc()
```

## 📋 Supported Formats
# Deezer
- MP3_128
- MP3_320 (SOMETIMES NEED PAID DEEZER)
- FLAC (PAID DEEZER ONLY)
# Spotify
- NORMAL
- HIGH
- VERY_HIGH

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚖️ License

This project is licensed under the GNU Affero General Public License v3 - see the 

LICENSE

 file for details.

## 🙏 Acknowledgments

- Original deezloader project
- Deezer API
- Spotify API
- Spotify Anon
- librespot-python
- librespot-auth
```