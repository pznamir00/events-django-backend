# Generated by Django 4.2.15 on 2024-08-29 20:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0004_auto_20211029_1451"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tickettemplate",
            old_name="_file",
            new_name="file",
        ),
    ]
