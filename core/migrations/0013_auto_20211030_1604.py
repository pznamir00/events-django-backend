# Generated by Django 3.2.8 on 2021-10-30 16:04

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_event_location"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="latitude",
        ),
        migrations.RemoveField(
            model_name="event",
            name="longitude",
        ),
        migrations.AlterField(
            model_name="event",
            name="location",
            field=django.contrib.gis.db.models.fields.PointField(
                geography=True, null=True, srid=4326
            ),
        ),
    ]
