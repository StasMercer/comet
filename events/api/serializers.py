from rest_framework import serializers

from accounts.models import CustomUser
from events.models import Event, Tag, Photo


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        lookup_field = 'name'


class ShortEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'avatar', 'date_expire')


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = '__all__'

    def to_representation(self, instance):
        return instance.img_value.path


class EventRegisterSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        many=False,
        queryset=CustomUser.objects.all(),
        slug_field='username'
    )

    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Event
        fields = ['name', 'description', 'time_begins', 'author', 'max_members', 'tags',
                  'avatar', 'date_expire', 'city', 'country']


class EventSerializer(serializers.ModelSerializer):

    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='name'
    )

    members_count = serializers.SerializerMethodField()

    author = serializers.SerializerMethodField()

    max_members = serializers.IntegerField(required=False, default=-1)

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'time_begins', 'author', 'members_count', 'max_members', 'tags',
                  'avatar', 'date_expire', 'city', 'country', 'geo']

    def get_event_photo(self, obj):
        qs = obj.event_photo.all()
        return PhotoSerializer(qs, many=True, read_only=True).data

    def get_author(self, obj):
        from accounts.api.serializers import ShortUserSerializer
        return ShortUserSerializer(obj.author).data

    def get_members_count(self, obj):
        return obj.members.count()
    #
    # def get_members(self, obj):
    #     qs = obj.members.all()
    #     return ShortUserSerializer(qs, many=True, read_only=True).data
    #
    # def get_tags(self, obj):
    #     qs = obj.tags.all()
    #     return TagSerializer(qs, many=True, read_only=True).data









