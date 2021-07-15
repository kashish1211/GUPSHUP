# Generated by Django 3.1.7 on 2021-07-15 13:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0019_auto_20210715_1916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='reporter',
        ),
        migrations.AddField(
            model_name='report',
            name='reporter',
            field=models.ManyToManyField(blank=True, related_name='reporter', to=settings.AUTH_USER_MODEL),
        ),
    ]
