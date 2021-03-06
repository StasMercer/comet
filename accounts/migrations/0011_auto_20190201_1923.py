# Generated by Django 2.1.5 on 2019-02-01 19:23

import cloudinary.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20190201_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='cloud_img',
            field=cloudinary.models.CloudinaryField(default=django.utils.timezone.now, max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='/users/a.jpg', upload_to='users/'),
        ),
    ]
