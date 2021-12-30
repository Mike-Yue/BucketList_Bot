# File for storing helper API functions
import json
import logging
import requests
import os

class ApiHelper():
    
    def __init__(self):
        # TODO
        # Move all Logging implementations to one class so I don't have to initialize it all the time in each module
        self.LOGGER = logging.getLogger(__name__)
        self.LOGGER.setLevel(logging.INFO)
        if (os.name == 'nt'):
            fh = logging.FileHandler("application_log.log")
        else:
            fh = logging.FileHandler("/var/log/bucketlistbot.log")
        fh.setLevel(logging.INFO)
        self.LOGGER.addHandler(fh)
        loggingFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(loggingFormat)

        self.facebookMessageBaseUrl = "https://graph.facebook.com/v2.6/me/messages?access_token="
        self.facebookUserDetailsBaseUrl = "https://graph.facebook.com/v2.6/"
        self.jsonHeadersType = {
            "Content-Type": "application/json"
        }
        
    def getPageAccessToken(self):
        if os.environ.get("PAGE_ACCESS_TOKEN") is None:
            raise KeyError("PAGE ACCESS TOKEN VARIABLE NOT SET")
        return os.environ.get("PAGE_ACCESS_TOKEN")

    def constructPostMessageUrl(self):
        return self.facebookMessageBaseUrl + self.getPageAccessToken()
    
    def getSenderName(self, fbId):
        try:
            userDetailParams = {
                "fields": "first_name",
                "access_token": self.getPageAccessToken()
            }
            userDetailsUrl = self.facebookUserDetailsBaseUrl + fbId
            userDetails = requests.get(userDetailsUrl, userDetailParams).json()
            return userDetails["first_name"]
        except KeyError:
            self.LOGGER.error("PAGE ACCESS TOKEN VARIABLE NOT SET")
        except requests.HTTPError as e:
            self.LOGGER.error("GET user details failed with error: " + str(e))
    
    def sendFacebookMessage(self, fbId, receivedMessage):
        try:
            facebookMessageUrl = self.constructPostMessageUrl()
            message = "Hi {}, {}".format(self.getSenderName(fbId), receivedMessage)
            responseMessage = json.dumps(
                {"recipient":{"id": fbId},
                "message": {"text": message}}
            )
            status = requests.post(facebookMessageUrl, headers=self.jsonHeadersType, data=responseMessage)
            self.LOGGER.info("Sent Message: {}".format(message))
        except KeyError:
            self.LOGGER.error("PAGE ACCESS TOKEN VARIABLE NOT SET")
        except requests.HTTPError as e:
            self.LOGGER.error("POST to Facebook failed with error: " + str(e))
    
