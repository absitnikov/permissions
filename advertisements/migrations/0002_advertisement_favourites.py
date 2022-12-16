# Generated by Django 4.1.4 on 2022-12-16 07:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('advertisements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='favourites',
            field=models.ManyToManyField(blank=True, related_name='favourites', to=settings.AUTH_USER_MODEL),
        ),
    ]
