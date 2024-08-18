# Generated by Django 3.2.8 on 2021-10-30 16:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_auto_20211030_1604"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventhistory",
            name="label",
            field=models.CharField(
                choices=[
                    ("1", "Moved"),
                    ("2", "Canceled"),
                    ("3", "Details Changed"),
                    ("4", "Took place"),
                ],
                max_length=1,
            ),
        ),
    ]
