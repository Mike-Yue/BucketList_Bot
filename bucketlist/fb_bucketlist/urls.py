from django.contrib import admin
from django.urls import path, include
from .views import bucketListBotView

urlpatterns = [
    path('pingbucketlistbot/', bucketListBotView.as_view()),
]