from typing import List

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from plotly.offline import init_notebook_mode, plot, iplot
import plotly.graph_objs as go

from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import pairwise_distances_argmin

import umap

from .features import SongFeatures


class Comparator():

    def __init__(self, scaler: str = None,
                 projector: str = 'pca',
                 plot_engine='plotly'):

        self.scaler = scaler
        self.projector = projector
        self._check_projector(self.projector)
        self._check_scaler(self.scaler)
        self.plot_engine = plot_engine
        self.fited_ = False

    def _check_scaler(self, scaler: str) -> None:
        """
        Safety param check 
        """
        avail_scalers = ['minmax', 'standard']
        if scaler in avail_scalers:
            pass
        elif scaler is None:
            pass
        else:
            raise ValueError('scaler value must be "minmax",'
                             ' "standard" or None')

    def _check_projector(self, projector: str) -> None:
        """
        Safety param check 
        """
        avail_projectors = ['pca', 'umap', 'tsne']
        if projector not in avail_projectors:
            raise ValueError(f'projector must be one of {avail_projectors}')

    def fit(self, bands_features: List[SongFeatures]):
        self.bands_features = bands_features
        self.bands_names = [band.band_name for band in bands_features]
        self.n_bands = len(self.bands_names)
        self.audio_features = bands_features[0].features

        self.features_all, self.band_names_long = self.concat_(
            self.bands_features)

        if self.scaler is not None:
            if self.scaler == 'minmax':
                scl = MinMaxScaler()

            elif self.scaler == 'standard':
                scl = StandardScaler()

            self.features_all = scl.fit_transform(self.features_all)

        if self.projector == 'pca':
            projector_ = PCA(n_components=2)

        elif self.projector == 'umap':
            projector_ = umap.UMAP()

        elif self.projector == 'tsne':
            projector_ = TSNE()

        self.projected_features = projector_.fit_transform(self.features_all)

        if self.plot_engine == 'plotly':
            self.plot_plotly()

        else:
            self.plot_()
        self.fited_ = True

    def concat_(self, df_list: List[SongFeatures]) -> pd.DataFrame:
        dfs = []
        band_names = []
        for df in df_list:
            features = df.loc[:, self.audio_features]
            dfs.append(features)
            band_names.extend([df.band_name] * len(features))
        df_all = pd.concat(dfs)
        return df_all, band_names

    def plot_(self):
        sns.scatterplot(self.projected_features[:, 0],
                        self.projected_features[:, 1],
                        hue=self.band_names_long,
                        style=self.band_names_long)

    def plot_plotly(self):
        palette = sns.palettes.color_palette('Set1', self.n_bands)
        traces = []
        for i, df in enumerate(self.bands_features):
            trace0 = go.Scatter(
                x=self.projected_features[np.array(
                    self.band_names_long) == df.band_name, 0],
                y=self.projected_features[np.array(
                    self.band_names_long) == df.band_name, 1],
                mode='markers',
                marker=dict(size=8,
                            color='rgb' + str(palette[i]),
                            opacity=0.8),
                text=df.name,
                name=df.band_name
            )
            traces.append(trace0)

        layout = go.Layout(
            hovermode='closest',
            autosize=False,
            width=1000,
            height=700)

        fig = go.Figure(data=traces, layout=layout)
        iplot(fig)


def most_similar_song(band1: SongFeatures,
                      band2: SongFeatures) -> pd.DataFrame:

    band1_feat = band1.loc[:, band1.features]
    band2_feat = band2.loc[:, band2.features]
    closests_idx = pairwise_distances_argmin(band1_feat, band2_feat)
    closest_songs = band2.data_frame.iloc[closests_idx, :]['name'].values

    df = pd.DataFrame({
        'name': band1.loc[:, 'name'],
        'closest': closest_songs
    })
    return df
