# Generated by Django 3.2.8 on 2021-10-29 12:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0003_rename_template_tickettemplate__file"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ticket",
            old_name="sold",
            new_name="is_sold",
        ),
        migrations.AddField(
            model_name="ticket",
            name="is_used",
            field=models.BooleanField(default=False),
        ),
    ]
