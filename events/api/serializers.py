from rest_framework import serializers

from accounts.models import CustomUser
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

    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='name'
    )
    members = serializers.SlugRelatedField(
        many=True,
        queryset=CustomUser.objects.all(),
        slug_field='username'
    )

    author = serializers.SlugRelatedField(
        many=False,
        queryset=CustomUser.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Event
        fields = ['name', 'author', 'members', 'views', 'tags', 'avatar', 'date_expire',]


    def get_event_photo(self, obj):
        qs = obj.event_photo.all()
        return PhotoSerializer(qs, many=True, read_only=True).data

    # def get_author(self, obj):
    #
    #     return ShortUserSerializer(obj.author).data
    #
    # def get_members(self, obj):
    #     qs = obj.members.all()
    #     return ShortUserSerializer(qs, many=True, read_only=True).data
    #
    # def get_tags(self, obj):
    #     qs = obj.tags.all()
    #     return TagSerializer(qs, many=True, read_only=True).data









