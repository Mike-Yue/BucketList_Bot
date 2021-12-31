from django.db import models

# Create your models here.
class Activity(models.Model):
    
    ACTIVITY_TYPE = (
        ("Food", "Food"),
        ("Drink", "Drink"),
        ("Hike", "Hike"),
        ("Sport", "Sport"),
        ("Other", "Other")
    )
    
    name = models.CharField(max_length=255)
    submitted_by = models.CharField(max_length=255)
    submission_date = models.DateField()
    activity_date = models.DateField(blank=True)
    activity_type = models.CharField(max_length=255, choices=ACTIVITY_TYPE)
    activity_address = models.CharField(max_length=511, blank=True)