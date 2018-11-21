from rest_framework import serializers
from events.models import Event, Tag, Photo
from accounts.api.serializers import ShortUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = '__all__'

    def to_representation(self, instance):
        return instance.img_value.path

class EventSerializer(serializers.ModelSerializer):

    tags = serializers.SerializerMethodField()
    event_photo = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['name', 'author', 'members', 'views', 'tags', 'event_photo']

    def get_author(self, obj):

        return ShortUserSerializer(obj.author).data

    def get_members(self, obj):
        qs = obj.members.all()
        return ShortUserSerializer(qs, many=True, read_only=True).data

    def get_tags(self, obj):
        qs = obj.tags.all()
        return TagSerializer(qs, many=True, read_only=True).data

    def get_event_photo(self, obj):
        qs = obj.event_photo.all()
        return PhotoSerializer(qs, many=True, read_only=True).data







