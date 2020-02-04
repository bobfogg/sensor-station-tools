import pandas as pd
from station.data import datafile

class GpsFile(datafile.DataFile):
    """Node Health File"""
    def __init__(self, filename):
        super(GpsFile, self).__init__(filename)

    def _clean(self):
        pass