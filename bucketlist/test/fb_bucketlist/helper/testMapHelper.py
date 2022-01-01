import unittest
from unittest.mock import patch

from fb_bucketlist.helper.mapHelper import MapHelper

class TestMapHelper(unittest.TestCase):
    testLongUrl = "https://www.google.com/maps/place/Cypress+Mountain/@49.396018,-123.2067337,17z/data=!3m1!4b1!4m5!3m4!1s0x548660d698f59675:0x821712a6c6d32ff3!8m2!3d49.396018!4d-123.204545"
    testShortUrl = "https://goo.gl/maps/9eet5QLAGv7eB2rUA"
    
    #Mock Google maps client so I don't make a service call everytime and spend extra money
    @patch("googlemaps.Client")
    def setUp(self, Client):
        self.mapHelper = MapHelper()
    
    def testfindNthOccurenceOfSubString(self):
        output = self.mapHelper.findNthOccurenceOfSubString("12345", "3", 1)
        self.assertEqual(output, 2)
        
    def testFindNthOccurenceOfSubStringEmptyString(self):
        output = self.mapHelper.findNthOccurenceOfSubString("", "1", 2)
        self.assertEqual(output, -1)
        
    def testFindNthOccurenceOfSubStringNoOccurence(self):
        output = self.mapHelper.findNthOccurenceOfSubString("1234567", "a", 2)
        self.assertEqual(output, -1)
        
    def testFindNthOccurenceOfSubStringLessOccurence(self):
        output = self.mapHelper.findNthOccurenceOfSubString("1234567", "1", 2)
        self.assertEqual(output, -1)

    def testGetCoordinatesFromUrl(self):
        coordinatesTuple = self.mapHelper.getCoordinatesFromUrl(self.testLongUrl)
        self.assertEquals(coordinatesTuple, ("49.396018", "-123.2067337"))
        
    def testGetLocationNameFromUrl(self):
        locationName = self.mapHelper.getLocationNameFromUrl(self.testLongUrl)
        self.assertEquals(locationName, "Cypress Mountain")