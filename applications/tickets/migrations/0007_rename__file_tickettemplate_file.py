# Generated by Django 4.2.15 on 2024-08-30 23:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0006_rename_file_tickettemplate__file"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tickettemplate",
            old_name="_file",
            new_name="file",
        ),
    ]
