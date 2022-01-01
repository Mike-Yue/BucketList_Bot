from enum import Enum
import logging
import os
from fb_bucketlist.helper.apiHelper import ApiHelper
from fb_bucketlist.helper.mapHelper import MapHelper
from fb_bucketlist.helper.stringOutputHelper import StringOutputHelper


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
if (os.name == 'nt'):
    fh = logging.FileHandler("application_log.log")
else:
    fh = logging.FileHandler("/var/log/bucketlistbot.log")
fh.setLevel(logging.INFO)
LOGGER.addHandler(fh)
loggingFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(loggingFormat)

#Enum class to contain all string output responses to the user
class States(Enum):
    CONFIRM_LOCATION = "Question 1" # Can you confirm this is the location you meant?
    CONFIRM_DATE = "Question 2" # What date are you going on?
    CONFIRM_TIME = "Question 3" # What time on that day?
    CONFIRM_ACTIVITY_TYPE = "Question 4" # Is this activity food, sports, etc etc
    CONFIRM_ACTIVITY_CREATION = "Statement 4" # I've created this event for you

nextStateMapping = {
    States.CONFIRM_LOCATION: States.CONFIRM_DATE,
    States.CONFIRM_DATE: States.CONFIRM_TIME,
    States.CONFIRM_TIME: States.CONFIRM_ACTIVITY_TYPE,
    States.CONFIRM_ACTIVITY_TYPE: States.CONFIRM_ACTIVITY_CREATION
}

stateToOutputMessageMapping = {
    States.CONFIRM_LOCATION: "".join((StringOutputHelper.USER_GREETING_OUTPUT.value, StringOutputHelper.CONFIRM_GOOGLE_MAPS_OUTPUT.value)),
    States.CONFIRM_DATE: StringOutputHelper.CONFIRM_DATE.value,
    States.CONFIRM_TIME: StringOutputHelper.CONFIRM_TIME.value,
    States.CONFIRM_ACTIVITY_TYPE: StringOutputHelper.CONFIRM_ACTIVITY_TYPE.value,
    States.CONFIRM_ACTIVITY_CREATION: StringOutputHelper.FINALIZE_GOOGLE_MAPS_ACTIVITY.value
}

apiHelper = ApiHelper()
mapHelper = MapHelper()

class ViewHelper():
    
    def trackStateAndSendMessage(self, fbId, messageReceived, userStates):
        print(userStates)
        try:
            if fbId not in userStates and "maps" in messageReceived:
                userStates[fbId] = States.CONFIRM_LOCATION
                locationDetails = mapHelper.getLocationDetails(messageReceived)
                userFirstName = apiHelper.getSenderName(fbId)
                apiHelper.sendFacebookMessage(fbId, stateToOutputMessageMapping[userStates[fbId]].format(userFirstName, locationDetails["name"], locationDetails["formatted_address"]))
                #Move state to next
                userStates[fbId] = nextStateMapping[userStates[fbId]]
            elif fbId not in userStates:
                apiHelper.sendFacebookMessage(fbId, messageReceived)
            elif userStates[fbId] not in nextStateMapping:
                apiHelper.sendFacebookMessage(fbId, stateToOutputMessageMapping[userStates[fbId]])
                #Remove userID from state as the conversation is now complete
                userStates.pop(fbId)
            else:
                apiHelper.sendFacebookMessage(fbId, stateToOutputMessageMapping[userStates[fbId]])
                #Move state to next
                userStates[fbId] = nextStateMapping[userStates[fbId]]
        except Exception as e:
            print(e)
            LOGGER.error(str(e))