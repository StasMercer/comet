from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from accounts.models import CustomUser
from events.models import Event, Tag, Photo


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


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
        fields = ['id', 'name', 'description', 'time_begins', 'author', 'avatar',
                  'max_members', 'tags', 'date_expire', 'city', 'country', 'geo']


class EventSerializer(serializers.ModelSerializer):
    from accounts.api.serializers import ShortUserSerializer

    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='name'
    )

    is_current_member = serializers.SerializerMethodField()

    members_count = serializers.SerializerMethodField()

    author = ShortUserSerializer()

    max_members = serializers.IntegerField(required=False, default=-1)

    current_user_follows_members = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'is_current_member', 'current_user_follows_members', 'name', 'description',
                  'time_begins', 'author', 'members_count', 'max_members', 'tags',
                  'avatar', 'date_expire', 'city', 'country', 'geo']


    def get_event_photo(self, obj):
        qs = obj.event_photo.all()
        return PhotoSerializer(qs, many=True, read_only=True).data

    def get_author(self, obj):
        from accounts.api.serializers import ShortUserSerializer
        return ShortUserSerializer(obj.author).data

    def get_members_count(self, obj):
        return obj.members.count()

    def get_is_current_member(self, obj):

        request = self.context.get('request', None)
        if request and request.user:
            is_member = Event.objects.filter(pk=obj.pk, members=request.user)
            if is_member:
                return True
            else:
                return False
        else:
            return False

    def get_current_user_follows_members(self, obj):
        from accounts.api.serializers import ShortUserSerializer
        request = self.context.get('request', None)
        if request and request.user:
            following = request.user.following.all()
            friends_in_events = set.intersection(set(following), set(obj.members.all()))
            if friends_in_events:

                result_objects = [ShortUserSerializer(e).data for e in friends_in_events]
                return result_objects
            else:
                return ''
        else:
            return ''

    # def get_members(self, obj):
    #     qs = obj.members.all()
    #     return ShortUserSerializer(qs, many=True, read_only=True).data
    #
    # def get_tags(self, obj):
    #     qs = obj.tags.all()
    #     return TagSerializer(qs, many=True, read_only=True).data









