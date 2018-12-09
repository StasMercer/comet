from django.db import models
from accounts.models import CustomUser
# Create your models here.


class Event(models.Model):

    avatar = models.ImageField(upload_to='events/')

    name = models.CharField(max_length=200, default='')

    description = models.TextField()

    date_created = models.DateField(auto_now_add=True)

    date_expire = models.DateField()

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='event_author')

    members = models.ManyToManyField(CustomUser, related_name='event_member')

    views = models.IntegerField(default=0)

    tags = models.ManyToManyField('Tag', related_name='event_tag')

    photos = models.ManyToManyField('Photo', related_name='event_photos')


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Photo(models.Model):
    ROLE_CHOICES = (('1', 'main'),
                    ('2', 'other'))

    role = models.CharField(choices=ROLE_CHOICES, max_length=1, default='2')

    img_value = models.ImageField(upload_to='events/', default='_')

    def __str__(self):
        return self.img_value.path

    def __unicode__(self):
        return '%d: %s' % (self.id, str(self.img_value.path))
