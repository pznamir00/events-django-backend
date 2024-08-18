# Generated by Django 3.2.8 on 2021-11-01 15:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0015_auto_20211101_1057"),
    ]

    operations = [
        migrations.AlterField(
            model_name="followedhashtag",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="followed_hashtags",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
