from enum import Enum

#Enum class to contain all string output responses to the user
class StringOutputHelper(Enum):
    USER_GREETING_OUTPUT = "Hi {}, "
    CONFIRM_GOOGLE_MAPS_OUTPUT = "can you confirm that {} at {} is the place you're trying to go to? Reply 'Yes' or 'No'."
    FINALIZE_GOOGLE_MAPS_ACTIVITY = "Got it. I've recorded down this activity!"
    WRONG_GOOGLE_MAPS_OUTPUT = "Sorry about that. I don't know how to deal with that at the moment. Please manually record the activity."
    