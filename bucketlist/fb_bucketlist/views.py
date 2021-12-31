from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import os
from .helper.apiHelper import ApiHelper
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
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('hub.verify_token', "1234") == '0808':
            LOGGER.info("Valid verify token received for webhook")
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            mapHelper = MapHelper()
            test = mapHelper.getLocation()
            print("poggers {}".format(test))
            LOGGER.error("Invalid verify token received")
            return HttpResponse('Error, invalid token')
    
    
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode("utf-8"))
        for entry in incoming_message["entry"]:
            for message in entry["messaging"]:
                if "message" in message:
                    LOGGER.info("Received message: " + message["message"]["text"])
                    apiHelper = ApiHelper()
                    if "maps" in message["message"]["text"]:
                        mapHelper = MapHelper()
                        address = mapHelper.getLocation(message["message"]["text"])
                        apiHelper.sendFacebookMessage(message["sender"]["id"], address)
                    else:
                        apiHelper.sendFacebookMessage(message["sender"]["id"], message["message"]["text"])
        return HttpResponse()
