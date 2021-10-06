# Generated by Django 3.2.7 on 2021-10-06 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_userplatformchoice_auth_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userplatformchoice',
            name='auth_data',
        ),
        migrations.AddField(
            model_name='userplatformchoice',
            name='auth_data_file',
            field=models.FileField(null=True, upload_to='static/auth_files'),
        ),
    ]
