from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import os
from .helper.viewHelper import ViewHelper
from .helper.viewHelper import convertDateFormat
from .helper.mapHelper import MapHelper

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

@method_decorator(csrf_exempt, name='dispatch')
class bucketListBotView(generic.View):
    
    viewHelper = ViewHelper()
    userStates = {}
    
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('hub.verify_token', "1234") == '0808':
            LOGGER.info("Valid verify token received for webhook")
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            LOGGER.error("Invalid verify token received")
            mapHelper = MapHelper()
            locationDetails = mapHelper.getLocationDetails('https://goo.gl/maps/ZAebeaSUgRNCh4xb9')
            print(convertDateFormat("09-09-2020"))
            self.viewHelper.trackStateAndSendMessage("1", "https://goo.gl/maps/8By4gqDYErQRDzwVA", self.userStates)
            return HttpResponse('Error, invalid token')
    
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode("utf-8"))
        for entry in incoming_message["entry"]:
            LOGGER.warn(str(entry))
            for message in entry["messaging"]:
                if "message" in message:
                    if "is_echo" in message["message"] and message["message"]["is_echo"]:
                        continue
                    LOGGER.info("Received message: " + message["message"]["text"])
                    self.viewHelper.trackStateAndSendMessage(message["sender"]["id"], message["message"]["text"], self.userStates)
        return HttpResponse()
