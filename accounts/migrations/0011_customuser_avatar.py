# Generated by Django 2.1.2 on 2018-11-16 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_customuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, default='/users/a.jpg', upload_to='<django.db.models.fields.CharField>/'),
        ),
    ]
