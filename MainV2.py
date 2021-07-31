#key BBFA0D08D3D99D2409C5D3D3F3A55B02

import requests
import json
import pprint
from pathlib import Path
from datetime import datetime
import time

urls = {
    "wishlist" : "https://store.steampowered.com/wishlist/id/Nijinskyvich/wishlistdata/",
    "playerSummary" : "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=BBFA0D08D3D99D2409C5D3D3F3A55B02&steamids=76561198250929424"
}

class API_Manager:
    def __init__(self,storageLocation,urls):
        self.storageLocation = storageLocation
        self.suffixes = {
            "program_data":"/program_data.txt",
            "app_data":"/app_data.txt"
        }
        self.urls = urls
        self.program_data = {}



        if not Path(self.suffixes["program_data"]).is_file():
            print("No program data file found, creating new file")
            self.program_data = {
                "last_called": str(time.time())
            }
            self.useFile(self.suffixes["program_data"],"w",self.program_data)

        else:
            print("Data file found")
            data = self.useFile(self.suffixes["program_data"],"r",)
            last_called = float(data["last_called"])
            print(last_called)
            print(time.time())
            if time.time() - last_called > 60:
                print("Requerying")
                pprint.pprint(self.scan("wishlist")["2100"])

            
    def scan(self,type):
        return json.loads(json.dumps(requests.get(self.urls[type]).json()))

    def useFile(self,location,mode,data = None):
        with open(location, mode) as file:
                if mode == "w":
                    json.dump(data, file)
                    return None
                if mode == "r":
                    return json.load(file)

            
    


apim = API_Manager("/Data",urls)




"""
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
response = requests.get(urls["wishlist"])


#jprint(response.json())
#print(response.status_code)
dataDict = json.loads(json.dumps(response.json()))

#for game in dataDict:
    #print(game)

#pprint.pprint(dataDict["2100"])

#pprint.pprint(json.loads(json.dumps(requests.get("https://store.steampowered.com/api/appdetails?appids=2100").json())))
"""
