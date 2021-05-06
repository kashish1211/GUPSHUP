# Generated by Django 3.1.7 on 2021-03-31 18:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0011_post_bookmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='downvote_comment',
            field=models.ManyToManyField(related_name='downvote_comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postcomment',
            name='upvote_comment',
            field=models.ManyToManyField(related_name='upvote_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]