from enum import Enum
import datetime
import logging
import os
from fb_bucketlist.helper.apiHelper import ApiHelper
from fb_bucketlist.helper.mapHelper import MapHelper
from fb_bucketlist.helper.stringOutputHelper import StringOutputHelper
from fb_bucketlist.models import Activity
from datetime import date

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
#TODO: Add an error handling state
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

def convertDateFormat(inputDate):
    try:
        return datetime.datetime.strptime(inputDate, "%m-%d-%Y").strftime("%Y-%m-%d")
    except ValueError as e:
        LOGGER.warn(e)
        return None
    except Exception as e:
        LOGGER.warn(e)
        return None

def confirmLocation(fbId, message, userStates, activity=None):
    locationDetails = mapHelper.getLocationDetails(message)
    userFirstName = apiHelper.getSenderName(fbId)
    activity.name = locationDetails["name"]
    activity.activity_address = locationDetails["formatted_address"]
    activity.save()
    apiHelper.sendFacebookMessage(fbId, stateToOutputMessageMapping[userStates[fbId]].format(userFirstName, locationDetails["name"], locationDetails["formatted_address"]))
    return True

def confirmDate(fbId, message, userStates, activity=None):
    if message.strip().casefold() == "yes".casefold():
        #TODO: Build activity model for address and title since User confirmed this is the right location
        #Send question asking them to confirm Date
        apiHelper.sendFacebookMessage(fbId, stateToOutputMessageMapping[userStates[fbId]])
        return True
    elif message.strip().casefold() == "no".casefold():
        apiHelper.sendFacebookMessage(fbId, StringOutputHelper.WRONG_GOOGLE_MAPS_OUTPUT.value)
        return False
    else:
        apiHelper.sendFacebookMessage(fbId, StringOutputHelper.INVALID_TEXT_OUTPUT.value)
        return False

def confirmTime(fbId, message, userStates, activity=None):
    #TODO: Build activity model for Date since User provided a date. Handle usecase if no date is provided
    # Also, add a check to make sure the given datetime isn't in the past. Joanne can probably take this
    if message and convertDateFormat(message) is not None:
        activity.activity_date = convertDateFormat(message.strip())
        activity.save()
    apiHelper.sendFacebookMessage(fbId, stateToOutputMessageMapping[userStates[fbId]])
    return True

def confirmActivityType(fbId, message, userStates, activity=None):
    try:
        activity.activity_time = message.strip()
        activity.save()
    except Exception as e:
        LOGGER.warn(e)
        #TODO: Build activity model for time since User provided a time. Handle usecase if no time is provided
    apiHelper.sendFacebookMessage(fbId, stateToOutputMessageMapping[userStates[fbId]])
    return True

def confirmActivityCreation(fbId, message, userStates, activity=None):
    try:
        activity.activity_type = message
        activity.save()
    except Exception as e:
        LOGGER.warn(e)
    #TODO: Build activity model for activity type since User provided a type. 
    # Then return a string that contains the entire object that's been created
    apiHelper.sendFacebookMessage(fbId, stateToOutputMessageMapping[userStates[fbId]])
    
    return True

def dateValidator(inputDate):
    # Joanne to implement checking passed in date to see if it's in the past.
    # Takes in a python Date object
    # Return true if in the past, false otherwise
    today = date.today()
    if (inputDate < today):
        return True
    else:
        return False

stateToFunctionMapping = {
    States.CONFIRM_LOCATION: confirmLocation,
    States.CONFIRM_DATE: confirmDate,
    States.CONFIRM_TIME: confirmTime,
    States.CONFIRM_ACTIVITY_TYPE: confirmActivityType,
    States.CONFIRM_ACTIVITY_CREATION: confirmActivityCreation
}

apiHelper = ApiHelper()
mapHelper = MapHelper()

class ViewHelper():
    
    userToActivityMap = {}
    
    def trackStateAndSendMessage(self, fbId, messageReceived, userStates):
        try:
            if fbId not in userStates and "maps" in messageReceived:
                self.userToActivityMap[fbId] = Activity()
                userStates[fbId] = States.CONFIRM_LOCATION
                self.userToActivityMap[fbId].submission_date = datetime.date.today()
                self.userToActivityMap[fbId].submitted_by = apiHelper.getSenderName(fbId)
                self.userToActivityMap[fbId].save()
                if(stateToFunctionMapping[userStates[fbId]](fbId, messageReceived, userStates, self.userToActivityMap[fbId])):
                    #Move state to next
                    userStates[fbId] = nextStateMapping[userStates[fbId]]
            elif fbId not in userStates:
                apiHelper.sendFacebookMessage(fbId, messageReceived)
            elif userStates[fbId] not in nextStateMapping:
                if(stateToFunctionMapping[userStates[fbId]](fbId, messageReceived, userStates, self.userToActivityMap[fbId])):
                    #Remove userID from state as the conversation is now complete
                    userStates.pop(fbId)
                    self.userToActivityMap.pop(fbId)
            else:
                if(stateToFunctionMapping[userStates[fbId]](fbId, messageReceived, userStates, self.userToActivityMap[fbId])):
                    #Move state to next
                    userStates[fbId] = nextStateMapping[userStates[fbId]]
        except Exception as e:
            LOGGER.error(str(e))