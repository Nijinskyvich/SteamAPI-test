#key BBFA0D08D3D99D2409C5D3D3F3A55B02

import requests
import json
#import pprint
from pathlib import Path
from datetime import datetime
import time

urls = {
    "wishlist" : "https://store.steampowered.com/wishlist/id/Nijinskyvich/wishlistdata/",
    "playerSummary" : "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=BBFA0D08D3D99D2409C5D3D3F3A55B02&steamids=76561198250929424"
}


#Probably going to only let it do wishlist stuff because effort
class API_Manager:
    def __init__(self,storageLocation,urls):
        self.storageLocation = storageLocation
        self.urls = urls
        self.program_data = {"last_called": float(time.time())}


        #This sets up the files in the event that the program has never been run before
        if not Path(self.storageLocation).is_file():
            print("No program data file found, creating new file")
            
            with open(self.storageLocation, "w") as outfile:
                json.dump(self.program_data, outfile)
                outfile.close()

            self.manage()

        else:
            
            # print("Data file found")

            with open(self.storageLocation) as json_file:
                self.program_data = json.load(json_file)
                self.program_data["last_called"] = float(self.program_data["last_called"])
                json_file.close()

            if time.time() - self.program_data["last_called"] > 1:
                self.program_data["last_called"] = float(time.time())
                self.manage()


    def query(self,type):
        #print("Querying " + str(type))
        return json.loads(json.dumps(requests.get(self.urls["wishlist"]).json()))

    def manage(self):
        entries = self.query("wishlist")
        

        for item in entries.keys():
            if item in self.program_data.keys():
                pass
            else:
                print(entries[item]["name"] + " has been added recently")
                self.program_data[item] = entries[item]["name"]
                
            try:
                discount_pct = entries[item]["subs"][0]["discount_pct"]
                price = entries[item]["subs"][0]["price"]
                if discount_pct > 0:
                    print(entries[item]["name"] + " is on sale for £"+str(price/100)+" at " +str(discount_pct) + "% off.")
            except:
                pass
        bad_shit = []
        for item in self.program_data.keys():
            if item not in entries.keys() and item != "last_called":
                print(self.program_data[item] + " has been removed recently, removing from storage.")
                bad_shit.append(item)
                

        for item in bad_shit:
            del self.program_data[item]

        with open(self.storageLocation, "w") as outfile:
            json.dump(self.program_data, outfile)

            outfile.close()

        self.end()


        #pprint.pprint(game_data)



        """
        for item in game_data.keys():
            if item in entries.keys():
                pass
            else:
                print(name+" removed from wishlist, deleted entry from database.")
        """
        
        
            #if item["sale"] == True:
                #print("On sale")


    def end(self):
        

        return


apim = API_Manager("Data/program_data.txt",urls)



#response = requests.get(urls["wishlist"])
#dataDict = json.loads(json.dumps(response.json()))
#pprint.pprint(dataDict["2100"])

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
