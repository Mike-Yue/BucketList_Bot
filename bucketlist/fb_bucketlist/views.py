from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
import logging
import os

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

# Create your views here.
class bucketListBotView(generic.View):
    def get(self, request, *args, **kwargs):
        
        if self.request.GET['hub.verify_token'] == '0808':
            LOGGER.info("Valid verify token received for webhook")
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            LOGGER.error("Invalid verify token received")
            return HttpResponse('Error, invalid token')

