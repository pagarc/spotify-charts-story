#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Use spotipy API wrapper to get audio features from scraped spotify charts data
"""

import pandas as pd
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify() 
cid = "YOUR_SPOTIFY_CLIENT_ID" 
secret = "YOUR_SPOTIFY_CLIENT_SECRET" 
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 
sp.trace = False 

spotify_charts = pd.read_csv("./SpotifyTop200GlobalDaily2017toNow.csv")

ids = spotify_charts['id'].tolist()

# Divide track ids into chunks of 100
chunks = [ids[x:x+100] for x in range(0, len(ids), 100)]

# List of lists of dictionaries
test = []

# For each chunk of 100, get audio features
for group in chunks:
    test.append(sp.audio_features(group))

# Flatten list
flat_list = [item for group in test for item in group]

# Convert to dataframe then export to CSV
features = pd.DataFrame(flat_list)
features.to_csv("./audioFeatures.csv")