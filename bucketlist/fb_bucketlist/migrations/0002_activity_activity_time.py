# Generated by Django 4.0 on 2022-01-01 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_bucketlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='activity_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
