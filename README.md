# Comparify

Compare artists songs from Spotify using the sound features available in the spotify official API.

## Installation

1. clone the repo

2. go to repo folder and type:

```bash
python setup.py install
```

## Tutorial

Comporify under de hood uses the official Spotify API ([spotipy](https://github.com/plamere/spotipy))
so you will need to create an authorized app token in Spotify Developer website: https://developer.spotify.com/

Then create a credentials manager with your `cliend_id` and `client_secret`:

```python
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '<your_client_token>'
client_secret = '<your_client_secret>'
credentials = SpotifyClientCredentials(client_id, client_secret)
```

Then create go to spotify and find out your artist of choice url. For example my band has the url https://open.spotify.com/artist/3rD7bBI9zkYhu62o79tWe6

The `artist_id` is the last characters of the url: 3rD7bBI9zkYhu62o79tWe6

Then you can start playing around with it simply doing:

```python
from comparify import SongFeatures

# one artist
dasouza = SongFeatures(credentials, '3rD7bBI9zkYhu62o79tWe6')
# another artist
malkmus = SongFeatures(credentials, '7wyRA7deGRxozTyBc6QXPe')
```

This returns a `SongFeatures` objects wich basically is a pandas.DataFrame with extra information. It has the atributes of a DataFrame so explore it as normally you would do:

```python
dasouza.head()
```

Then instance the `Comparaton` with or without arguments for defaults:

```python
from comparify import Comparator
comparator = Comparator(scaler='minmax', projector='tsne')
comparator.fit([dasouza, malkmus])
```

And you will get a beautifull plotly scatter with the projected features in a 2d space.