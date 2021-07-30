# Generated by Django 3.1.7 on 2021-07-30 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0025_auto_20210730_1602'),
        ('users', '0011_auto_20210707_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followed_category',
            field=models.ManyToManyField(related_name='followed_category', to='blog.Category'),
        ),
    ]