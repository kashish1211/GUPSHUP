# Generated by Django 3.1.7 on 2021-07-06 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210706_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image_url',
            field=models.URLField(default='http://127.0.0.1:8000/media/default2.png'),
        ),
    ]