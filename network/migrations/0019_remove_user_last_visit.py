# Generated by Django 3.0.8 on 2020-07-27 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0018_user_last_visit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_visit',
        ),
    ]
