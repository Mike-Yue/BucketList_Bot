from django.db import models
from django.utils import timezone

# Create your models here.
class Activity(models.Model):
    
    ACTIVITY_TYPE = (
        ("Food", "Food"),
        ("Drink", "Drink"),
        ("Hike", "Hike"),
        ("Sport", "Sport"),
        ("Other", "Other")
    )
    
    name = models.CharField(max_length=255, default="Placeholder")
    submitted_by = models.CharField(max_length=255, default="Placeholder")
    submission_date = models.DateField(auto_now_add=timezone.now())
    activity_date = models.DateField(blank=True, null=True)
    activity_time = models.TimeField(blank=True, null=True)
    activity_type = models.CharField(max_length=255, choices=ACTIVITY_TYPE, default="Other")
    activity_address = models.CharField(max_length=511, blank=True, null=True)
    
    def __str__(self):
        return self.name