# Generated by Django 3.0.8 on 2020-07-28 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0019_remove_user_last_visit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-post_time']},
        ),
    ]
