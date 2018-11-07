import math

import numpy as np
import pandas as pd

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

#hello

class SongsDataFrame():
    def __init__(self, credentials_manager, band_id):
        self.spotify = spotipy.Spotify(
            client_credentials_manager=credentials_manager)

        self.band_id = band_id
        self.band_name = self.spotify.artist(band_id)['name']

        self.features = ['energy',
                         'duration_ms',
                         'loudness',
                         'valence',
                         'danceability',
                         'tempo',
                         'speechiness',
                         'instrumentalness',
                         'acousticness',
                         'liveness']

        self.album_ids_name = self.get_album_ids_names(
            self.spotify, self.band_id)
        self.album_ids = self.album_ids_name.keys()
        self.data_frame = self.generate_df(self.album_ids)

    def get_album_ids_names(self, service, band_id) -> dict:
        albums_all = service.artist_albums(band_id)
        # filter singles and compilations
        albums = [a for a in albums_all['items']
                  if a['album_type'] not in ['single', 'compilation']]

        # secure filter in case of wrong artist
        band_albums = [a for a in albums
                       if a['artists'][0]['name'] == self.band_name]

        album_id_to_name = {a['id']: a['name'] for a in band_albums}

        return album_id_to_name

    def get_track_features(self, songs):
        track_ids = [foo['id'] for foo in songs]
        chunk_size = 50
        num_chunks = int(math.ceil(len(track_ids) / float(chunk_size)))
        features_add = []
        for i in range(num_chunks):
            chunk_track_ids = track_ids[i*chunk_size:(i+1)*chunk_size]
            chunk_features = self.spotify.audio_features(tracks=chunk_track_ids)
            features_add.extend(chunk_features)

        features_df = pd.DataFrame(features_add)
        features_df = features_df[self.features] # filter features
        return features_df

    def generate_df(self, album_ids):
        songs_df_data = []
        for album_id in album_ids:
            # get songs in the album
            songs = self.spotify.album_tracks(album_id=album_id)['items']
            features = self.get_track_features(songs)
            features = features.values.tolist()
            for (track, feature) in zip(songs, features):
                t = track
                this_row = [t['id'], t['name'], album_id]
                this_row.extend(feature)
                songs_df_data.append(this_row)
        columns = ['id', 'name', 'album'] + self.features
        songs_df = pd.DataFrame(songs_df_data, columns=columns).drop_duplicates(subset='id')
        songs_df.album.replace(self.album_ids_name, inplace=True)
        return songs_df
