from typing import List

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap

from .features import SongFeatures

class Comparator():

    def __init__(self, scaler:str=None, projector:str='pca'):
        self.scaler = scaler
        self.projector = projector
        self._check_projector(self.projector)
        self._check_scaler(self.scaler)
        
    def _check_scaler(self, scaler:str) -> None:
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
    
    def _check_projector(self, projector:str) -> None:
        """
        Safety param check 
        """
        avail_projectors = ['pca', 'umap', 'tsne']
        if projector not in avail_projectors:
            raise ValueError(f'projector must be one of {avail_projectors}')

    def fit(self, bands_features: List[SongFeatures]):
        self.bands_features = bands_features

        self.bands_names = [band.bands_names for band in bands_features]

