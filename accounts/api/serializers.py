from rest_framework import serializers
from rest_framework.relations import RelatedField
from rest_framework.validators import UniqueValidator
from accounts.models import CustomUser, Rate, UserPhoto
from events.api.serializers import TagSerializer, ShortEventSerializer
from events.models import Tag

def rate_validator(value):
    if value > 5 or value < 0:
        raise serializers.ValidationError('rate is incorrect')


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhoto
        fields = '__all__'


class ShortUserSerializer(serializers.ModelSerializer):

    user_rate = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'avatar', 'first_name', 'last_name', 'user_rate']

    def get_user_rate(self, obj):
        qs = Rate.objects.filter(to_user__username=obj.username)
        sum = 0

        if len(qs) > 0:
            for obj in qs:
                sum += obj.value
            return sum / len(qs)
        else:
            return 0


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=6)

    class Meta:
        lookup_field = 'username'
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'date_of_birth']

        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )

    user_photos = PhotoSerializer(many=True)

    events_created = serializers.SerializerMethodField()

    user_rate = serializers.SerializerMethodField()

    events_visited = serializers.SerializerMethodField()

    tags = TagSerializer(many=True)

    followers = serializers.SerializerMethodField()

    following = serializers.SerializerMethodField()


    class Meta:
        model = CustomUser
        lookup_field = 'username'
        fields = ('email', 'username', 'first_name', 'last_name',
                  'avatar', 'cloud_img', 'date_of_birth', 'tags', 'events_created', 'events_visited',
                  'user_rate', 'followers', 'following', 'user_photos', 'city', 'country')
        read_only_fields = ('username', 'email', 'rate')
        depth = 1
        extra_kwargs = {

            'url': {'lookup_field': 'username'}
        }

    def get_user_photos(self, obj):
        qs = obj.user_photos.all()
        return PhotoSerializer(qs, many=True, read_only=True).data


    def get_followers(self, obj):
        return obj.followers.count()

    def get_following(self, obj):
        return obj.following.count()

    def get_events_created(self, obj):
        qs = obj.event_author.all()
        return ShortEventSerializer(qs, many=True, read_only=True).data

    def get_events_visited(self, obj):
        qs = obj.event_member.all()
        return ShortEventSerializer(qs, many=True, read_only=True).data

    def get_user_rate(self, obj):
        qs = Rate.objects.filter(to_user__username=obj.username)
        sum = 0

        if len(qs) > 0:
            for obj in qs:
                sum += obj.value
            return sum / len(qs)
        else:
            return 0




class RateSerializer(serializers.ModelSerializer):
    from_user = serializers.SlugRelatedField(
        many=False,
        queryset=CustomUser.objects.all(),
        slug_field='username'
    )

    to_user = serializers.SlugRelatedField(
        many=False,
        queryset=CustomUser.objects.all(),
        slug_field='username'
    )

    value = serializers.IntegerField(
        required=True,
        validators=[rate_validator]
    )

    class Meta:
        model = Rate
        fields = '__all__'

    def create(self, validated_data):
        try:
            qs = Rate.objects.get(from_user=validated_data['from_user'], to_user=validated_data['to_user'])
        except Rate.DoesNotExist:
            qs = None


        if qs is not None:
            rate = qs
            rate.value = validated_data['value']
            rate.save()
        else:
            rate = Rate.objects.create(**validated_data)

        return rate








