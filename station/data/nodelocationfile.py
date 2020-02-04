import pandas as pd
import utm
from station.data import datafile

class NodeLocationFile(datafile.DataFile):
    """Node Location File Encapsulation
    expected fields: NodeId, lat, lng"""
    def __init__(self, filename):
        super(NodeLocationFile, self).__init__(filename)

    def _clean(self):
        """append utm"""
        self.df = self.append_utm(self.df)

    def append_utm(self, df):
        """append utm x,y,zone,letter to dataframe"""
        xs = []
        ys = []
        zones = []
        letters = []
        for i, record in df.iterrows():
            (x,y,zone,letter) = utm.from_latlon(record.lat, record.lng)
            xs.append(x)
            ys.append(y)
            zones.append(zone)
            letters.append(letter)
        df['x'] = xs
        df['y'] = ys
        df['zone'] = zones
        df['letter'] = letters
        return df

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    data = NodeLocationFile(filename)
    print(data.df)