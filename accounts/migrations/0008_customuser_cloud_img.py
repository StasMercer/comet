# Generated by Django 2.1.5 on 2019-02-01 18:57

import cloudinary.models
from django.db import migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20181215_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='cloud_img',
            field=cloudinary.models.CloudinaryField(default=django.utils.timezone.now, max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
    ]