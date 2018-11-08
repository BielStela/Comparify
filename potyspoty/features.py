import math

import numpy as np
import pandas as pd

import spotipy


class SongFeatures():
    """
    Spotify API accessor to retrieve a DataFrame with song features
    given a band ID.

    Requires and instance of SpotifyClientCredentials.
    """

    def __init__(self, credentials_manager, band_id,
                 include_singles=False, include_compilations=False):

        self.spotify = spotipy.Spotify(
            client_credentials_manager=credentials_manager)

        self.band_id = band_id
        self.band_name = self.spotify.artist(band_id)['name']

        self.features = ['duration_ms',
                         'loudness',
                         'energy',
                         'valence',
                         'danceability',
                         'tempo',
                         'speechiness',
                         'instrumentalness',
                         'acousticness',
                         'liveness']

        self.albums = self.album_ids_names(self.spotify, self.band_id,
                                           include_singles,
                                           include_compilations)

        self.album_ids = self.albums.keys()
        self.data_frame = self.generate_df(self.album_ids)

    def album_ids_names(self, service, band_id: str, include_singles=False,
                        include_compilations=False) -> dict:
        """
        Returns a dict with the albums ids as keys and album names as value
        """
        albums_all = service.artist_albums(band_id)

        album_type_filter = ['single', 'compilation']

        if include_singles:
            album_type_filter = ['compilation']

        elif include_compilations:
            album_type_filter = ['single']

        elif include_compilations and include_singles:
            albums = albums_all

        # filter singles and compilations
        albums = [a for a in albums_all['items']
                  if a['album_type'] not in album_type_filter]

        # secure filter in case of wrong artist
        band_albums = [a for a in albums
                       if a['artists'][0]['name'] == self.band_name]

        album_id_to_name = {a['id']: a['name'] for a in band_albums}

        return album_id_to_name

    def get_track_features(self, songs) -> pd.DataFrame:
        """
        Gets track features by chunks of 50
        """
        track_ids = [foo['id'] for foo in songs]
        chunk_size = 50
        num_chunks = math.ceil(len(track_ids) / float(chunk_size))
        features_add = []

        for i in range(num_chunks):
            chunk_track_ids = track_ids[i*chunk_size:(i+1)*chunk_size]
            chunk_features = self.spotify.audio_features(
                tracks=chunk_track_ids)
            features_add.extend(chunk_features)

        features_df = pd.DataFrame(features_add)
        features_df = features_df[self.features]  # filter features
        return features_df

    def generate_df(self, album_ids) -> pd.DataFrame:
        """
        Returns pd.DataFrame of all tracks
        """
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
        songs_df = pd.DataFrame(songs_df_data,
                                columns=columns).drop_duplicates(subset='id')

        # replace album ids by name
        songs_df.album.replace(self.albums, inplace=True)
        return songs_df
