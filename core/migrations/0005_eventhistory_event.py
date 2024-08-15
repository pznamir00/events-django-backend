# Generated by Django 3.2.8 on 2021-10-27 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_rename_id_event_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventhistory",
            name="event",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="histories",
                to="core.event",
            ),
        ),
    ]
