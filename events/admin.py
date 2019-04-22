from django.contrib import admin
from .models import Event, Tag, Photo
# Register your models here.
admin.site.register(Event)
admin.site.register(Tag)
admin.site.register(Photo)