#!/usr/bin/env python
"""
"""

# Put in imports
import pandas as pd
import requests

class Records:
    def __init__(self, genusKey=None, year=None):
        # store input params
        self.genusKey = genusKey
        self.year = year
        
        # will be used to store output results
        self.df = []
        self.json = pd.DataFrame()
        
    def get_single_batch(self, offset=0, limit=20):
        """
        Returns a GBIF REST query with records between offset
        and offset + limit in JSON format. The genusKey and 
        year interval can be changed.
        """
        res = requests.get(
            url="https://api.gbif.org/v1/occurrence/search/",
            params={
                "genusKey": self.genusKey,
                "year": self.year,
                "offset": offset,
                "limit": limit,
                "hasCoordinate": "true",
                "country": "US",
            }
        )
        return res.json()
        
    def get_all_records(self):
        """
        Store the JSON results to the instance object, 
        storing JSON as a dictionary to self.json and 
        as a dataframe to self.df
        """
        offset = 0
        while 1: 
            # get JSON data for a batch 
            jdata = self.get_single_batch(offset, 300)
            # increment counter by 300 (the max limit)
            offset += 300
            # add this batch of data 
            self.json.extend(jdata["results"])
            # stop when end of record is reached
            if jdata["endOfRecords"]:
                break
                # print a dot on each rep to show progress
                print('.', end='')

        #results to dataframe
        self.df = pd.json_normalize(self.json)
        

if __name__ == "__main__":

