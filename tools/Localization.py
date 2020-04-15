import csv
from station.locate.api import LocationApi
import datetime
import pandas as pd
import sys
import json

# Update this to point to your senosr 
beep_filename = 'beeps.csv'
# node file with lat/lng data for node ids:  required NodeId,lat,lng fields
node_filename = 'node-locations.csv'
# Tag File Location - required fields:  TagId
tag_filename = 'tags-to-analyze.csv'
tags = []
with open(tag_filename, 'r') as inFile:
    reader = csv.DictReader(inFile)
    for row in reader:
        tags.append(row['TagId'].strip())

api = LocationApi(
    beep_filename=beep_filename,
    node_filename=node_filename
)

def get_locations(freq):
    # dataframes with calculated stats
    dfs = []
    # loop through all the tags
    for tag in tags:
        # loop through all the Radio Channels
        for channel in api.nodedata.channels():
            print('locating tag {}; channel {};'.format(tag, channel))
            begin = datetime.datetime.utcnow()
            df= api.weighted_average(freq=freq, tag_id=tag.upper(), channel=channel)
            delta = datetime.datetime.utcnow() - begin
            print('weighted average complete {}'.format(delta))
            df['TagID'] = tag
            df['channel'] = channel
            dfs.append(df)

    df = pd.concat(dfs)
    # potentially useful columns to append
    df['date'] = df.index.strftime('%Y-%m-%d')
    df['time_of_day'] = df.index.strftime('%H:%M:%S')
    df['hour'] = pd.to_numeric(df.index.strftime('%H'))

    filename = 'estimates_{}.csv'.format(freq)
    df.dropna().to_csv(filename)

# resmample frequency for location estimates
# T=minutes, S=seconds, H=hours - ex:    30S, 60S, 1T, 5T, 15T, 30T, ...

freq = '60T'
for freq in ['5T', '15T', '30T', '60T', '120T']:
    get_locations(freq)