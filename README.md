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

This returns a `SongFeatures` objects which basically is a `pandas.DataFrame` with extra information. It has the attributes of a `DataFrame`:

```python
dasouza.head(5)
```
id|name|album|loudness|energy|valence|danceability|tempo|speechiness|instrumentalness|acousticness|liveness
---|---|---|---|---|---|---|---|---|---|---|---
4aaco211p3HFubmFfBoaxj|Noves Venècies|Futbol d'Avantguarda|-8.716|0.356|0.608|0.582|130.898|0.0321|0.126|0.452|0.118
4N5E7jIK4Ti9yXoshshQ1J|Migracions de salmons|Futbol d'Avantguarda|-7.193|0.61|0.657|0.535|125.95|0.0299|0.255|0.134|0.131
0hdwI9Xf7GnJUyUmXNETt0|Finals|Futbol d'Avantguarda|-6.603|0.61|0.72|0.638|130.071|0.0304|0.0491|0.0598|0.14 0
ERzbcM3uYCmH0zuONy02y|Tan enfora|Futbol d'Avantguarda|-6.709|0.723|0.537|0.607|120.025|0.0285|0.162|0.216|0.228
2IjcG82yOERIFe9bV4dWrL|Dos microbis|Futbol d'Avantguarda|-9.703|0.422|0.384|0.375|153.432|0.0424|0.525|0.622|0.0983




Then instance the `Comparator`:

```python
from comparify import Comparator
comparator = Comparator(scaler='minmax', projector='tsne')
comparator.fit([dasouza, malkmus])
```

And you will get a plotly scatter with the projected features in a 2d space. 

Also you can get a the most similar song (euclidian distance based) with `most_similar_song()`

```python
from comparify import most_similar_song

most_similar_song(dasouza, malkmus)
```

name|closest
---|---
Noves Venècies|Senator
Migracions de salmons|Tigers
Finals|Senator
Tan enfora|1% Of One
Dos microbis|Us

### Disclaimer

This is a toy project so feel free to say me anything or sue me because of my bad abstractions.