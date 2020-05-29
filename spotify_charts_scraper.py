#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get Spotify Charts data from https://spotifycharts.com/regional/global/daily/
"""

import pandas as pd
from bs4 import BeautifulSoup
from requests import get
from time import time, sleep
from datetime import datetime, timedelta
from random import randint
from warnings import warn
from IPython.core.display import clear_output

# Lists to store the scraped data in
dates = []
positions = []
tracks = []
artists = []
streams = []
covers = []
urls = []

# Prepare loop monitoring
start_time = time()
request = 0

# Modify url to crawl through Spotify Charts website pages
days = [str(d) for d in pd.date_range("2017-01-01", datetime.today() - timedelta(1)).date]

# Header
headers = {'Accept-Language': 'en-US, en;q=0.5'}

# For every day from 2017-01-01 to yesterday
for day in days:

    # Make get request
    response = get('https://spotifycharts.com/regional/global/daily/' + day, headers = headers)

    # Pause loop
    sleep(randint(2,4))

    # Monitor requests
    request += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(request, request/elapsed_time))
    clear_output(wait = True)

    # Throw warning for non-200 status codes
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(request, response.status_code))

    # Break loop if the number of requests is greater than expected
    if request > 1500:
        warn('Number of requests was greater than expected.')
        break

    # Parse request content with BeautifulSoup
    bs = BeautifulSoup(response.text, 'html.parser')
    
    # Select all track containers from a single page
    track_containers = bs.select('tbody tr')

    # Scrape html elements
    for container in track_containers:
        # get date
        dates.append(day)
        
        # Get url
        url = container.find('a').get('href')
        urls.append(url)
        
        # Get album cover art
        cover = container.find('a').find('img').get('src')
        covers.append(cover)
    
        # Get position
        position = container.find('td',{'class':'chart-table-position'}).text
        positions.append(position)
        
        # Get track container
        track = container.find('td',{'class':'chart-table-track'})
        
        # Get track title
        title = track.find('strong').text
        tracks.append(title)

        # Get track artist
        artist = track.find('span').text[3:] # remove "by "
        artists.append(artist)

        # Get number of streams
        stream = container.find('td',{'class':'chart-table-streams'}).text
        streams.append(stream)


# Store scraped lists in dataframe    
chart_data = pd.DataFrame({
    'Date': dates,
    'Position': positions,
    'Track Name': tracks,
    'Artist': artists,
    'Streams': streams,
    'Album Art': covers,
    'URL': urls
})

# Remove commas from streams
chart_data['Streams'] = chart_data['Streams'].replace(',', '', regex = True)

# Make streams column numeric
chart_data['Streams'] = chart_data['Streams'].apply(pd.to_numeric, errors = 'coerce')

# Create id column from URLs
chart_data['id'] = chart_data.URL.str[31:]

# Print dataframe information and first few rows
print(chart_data.info())
print(chart_data.head())

# Export dataframe to csv in current file path
chart_data.to_csv("./SpotifyTop200GlobalDaily2017toNow.csv", index = False, encoding='utf-8-sig')
