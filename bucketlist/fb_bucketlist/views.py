from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
import logging
import os

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
fh = logging.FileHandler(os.getcwd() + "/application_log.log")
fh.setLevel(logging.INFO)
LOGGER.addHandler(fh)
loggingFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(loggingFormat)

# Create your views here.
class bucketListBotView(generic.View):
    def get(self, request, *args, **kwargs):
        LOGGER.info("Reached bucketlistbot Webhooks")
        return HttpResponse("Hello World")

