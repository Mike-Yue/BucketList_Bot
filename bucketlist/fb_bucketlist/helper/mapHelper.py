from django.conf import settings

import googlemaps
import requests
import urllib.parse
import os

class MapHelper():
    
    def __init__(self):
        if (os.environ.get("MAPS_API_KEY")):
            self.gmaps = googlemaps.Client(key=os.environ.get("MAPS_API_KEY"))
        else:
            # For local window dev just read it from a txt file
            with open(os.path.join(settings.BASE_DIR, "maps_api_key.txt")) as f:
                key = f.read()
            self.gmaps = googlemaps.Client(key=key)
    
    # Method used to parse addresses and URLs
    def findNthOccurenceOfSubString(self, baseString, subString, n):
        start = baseString.find(subString)
        while start >= 0 and n > 1:
            start = baseString.find(subString, start+len(subString))
            n -= 1
        return start
    
    def getCoordinatesFromUrl(self, longUrl):
        startIndex = self.findNthOccurenceOfSubString(longUrl, "@", 1)
        longUrl = str(longUrl)[startIndex+1:]
        endIndex = self.findNthOccurenceOfSubString(longUrl, ",", 2)
        coordinatesList = longUrl[:endIndex].split(",")
        return (coordinatesList[0], coordinatesList[1])
        
    def getLocationNameFromUrl(self, longUrl):
        startIndex = self.findNthOccurenceOfSubString(longUrl, "https://www.google.com/maps/place/", 1)
        longUrl = longUrl[startIndex+len("https://www.google.com/maps/place/"):]
        endIndex = self.findNthOccurenceOfSubString(longUrl, "/", 1)
        return urllib.parse.unquote(longUrl[:endIndex]).replace("+", " ")
    
    # gmaps.places returns a list of locations that matches our search term
    # Return the first one since that's most likely the one that we meant
    # Will expand to return all locations at a future date
    def getLocationDetails(self, mapsUrl): 
        session = requests.Session()
        resp = session.head(mapsUrl, allow_redirects=True)
        coordinates = self.getCoordinatesFromUrl(resp.url)
        locationName = self.getLocationNameFromUrl(resp.url)
        
        # Aside from name and formatted_address, can also access key "types" to get a list
        # of categories this location is tagged with, such as ["Restaurant", "Food", "Establishment"]
        # For full list of types, refer to https://developers.google.com/maps/documentation/places/web-service/supported_types
        # Can also access the "business_status" field to see if location is OPERATIONAL, which may be helpful
        return self.gmaps.places(query=locationName, location=coordinates)["results"][0]
        
        

