from enum import Enum
import logging
import os
from fb_bucketlist.helper.apiHelper import ApiHelper


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

class ViewHelper():
    
    userStates = {}
    
    def trackStateAndSendMessage(self, fbId, messageReceived):
        try:
            if fbId not in self.userStates and "maps" in messageReceived:
                self.userStates[fbId] = States.CONFIRM_LOCATION
                LOGGER.info("User {} currently at state {}".format(fbId, self.userStates[fbId].value))
                #TODO: Send message
                ApiHelper().sendFacebookMessage(fbId, "User {} currently at state {}".format(fbId, self.userStates[fbId].value))
                #Move state to next
                self.userStates[fbId] = nextStateMapping(self.userStates[fbId])
            elif self.userStates[fbId] not in nextStateMapping:
                #TODO Send confirmation message
                ApiHelper().sendFacebookMessage(fbId, "User {} currently at state {} and has finished setup".format(fbId, self.userStates[fbId].value))
                #Remove userID from state as the conversation is now complete
                self.userStates.pop(fbId)
            else:
                #TODO: send message
                ApiHelper().sendFacebookMessage(fbId, "User {} currently at state {}".format(fbId, self.userStates[fbId].value))
                #Move state to next
                self.userStates[fbId] = nextStateMapping(self.userStates[fbId])
        except Exception as e:
            LOGGER.error(str(e))