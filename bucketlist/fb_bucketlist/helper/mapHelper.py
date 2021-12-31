import googlemaps
import requests
import urllib.parse
import os

class MapHelper():
    
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
        print(urllib.parse.unquote(longUrl[:endIndex]))
        return urllib.parse.unquote(longUrl[:endIndex])
    
    def getLocation(self, mapsUrl): 
        key = os.environ.get("MAPS_API_KEY")
        gmaps = googlemaps.Client(key=key)
        test_url = mapsUrl
        session = requests.Session()
        resp = session.head(test_url, allow_redirects=True)
        print(resp.url)
        locationName = self.getLocationNameFromUrl(resp.url)
        coordinatesTuple = self.getCoordinatesFromUrl(resp.url)
        print(coordinatesTuple)
        return gmaps.places(query=locationName)["results"][0]["formatted_address"]
        
        

