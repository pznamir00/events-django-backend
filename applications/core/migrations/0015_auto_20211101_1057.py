# Generated by Django 3.2.8 on 2021-11-01 10:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0014_alter_eventhistory_label"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="is_active",
        ),
        migrations.AddField(
            model_name="event",
            name="canceled",
            field=models.BooleanField(default=False),
        ),
    ]
