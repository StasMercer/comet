import datetime
from cloudinary.models import CloudinaryField
from django.db import models
from accounts.models import CustomUser
# Create your models here.


class Event(models.Model):

    avatar = CloudinaryField('image', blank=True)

    name = models.CharField(max_length=200, default='')

    description = models.TextField()

    date_created = models.DateField(auto_now_add=True)

    date_expire = models.DateField()

    time_begins = models.TimeField(default=datetime.time(16, 00))

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='event_author')

    members = models.ManyToManyField(CustomUser, related_name='event_member')

    max_members = models.IntegerField(default=-1)

    views = models.IntegerField(default=0)

    tags = models.ManyToManyField('Tag')

    country = models.CharField(max_length=30)

    city = models.CharField(max_length=30)

    geo = models.CharField(max_length=100)


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%s'% (self.name)


class Photo(models.Model):
    ROLE_CHOICES = (('1', 'main'),
                    ('2', 'other'))

    role = models.CharField(choices=ROLE_CHOICES, max_length=1, default='2')

    img_value = CloudinaryField('image')

    def __str__(self):
        return self.img_value.path

    def __unicode__(self):
        return '%d: %s' % (self.id, str(self.img_value.path))
