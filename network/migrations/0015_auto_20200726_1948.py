# Generated by Django 3.0.8 on 2020-07-26 13:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0014_auto_20200726_1937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='user_follower',
        ),
        migrations.AddField(
            model_name='follow',
            name='user_follower',
            field=models.ManyToManyField(blank=True, null=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='follow',
            name='user_following',
        ),
        migrations.AddField(
            model_name='follow',
            name='user_following',
            field=models.ManyToManyField(blank=True, null=True, related_name='followings', to=settings.AUTH_USER_MODEL),
        ),
    ]