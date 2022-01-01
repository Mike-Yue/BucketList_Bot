from enum import Enum

#Enum class to contain all string output responses to the user
class StringOutputHelper(Enum):
    USER_GREETING_OUTPUT = "Hi {}, "
    CONFIRM_GOOGLE_MAPS_OUTPUT = "can you confirm that {} at {} is the place you're trying to go to? Reply 'Yes' or 'No'."
    FINALIZE_GOOGLE_MAPS_ACTIVITY = "Got it. I've recorded down this activity!"
    WRONG_GOOGLE_MAPS_OUTPUT = "Sorry about that. I don't know how to deal with that at the moment. Please manually record the activity."
    CONFIRM_DATE = "Do you know which day you're going? If yes, give me a date in MM-DD-YYYY format. If not, type no"
    CONFIRM_TIME = "Do you know what time you're going. If yes, give me a time in 24H HH:MM format. If not, type no"
    CONFIRM_ACTIVITY_TYPE = "What activity type is it? (Food/Drink/Sport/Hike/Other)"
    