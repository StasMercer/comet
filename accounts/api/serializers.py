from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts.models import CustomUser, Rate, UserPhoto



def rate_validator(value):
    if value > 5 or value < 0:
        raise serializers.ValidationError('rate is incorrect')


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('friends',)


class ShortUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'avatar', 'first_name', 'last_name']


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


    user_photos = serializers.SerializerMethodField()

    events_created = serializers.SerializerMethodField()

    user_rate = serializers.SerializerMethodField()

    events_visited = serializers.SerializerMethodField()


    class Meta:
        model = CustomUser
        lookup_field = 'username'
        fields = ('email', 'username', 'first_name', 'last_name',
                  'avatar', 'date_of_birth', 'tags', 'events_created', 'events_visited',
                  'user_rate', 'friends', 'user_photos')
        read_only_fields = ('username', 'email')
        extra_kwargs = {

            'url': {'lookup_field': 'username'}
        }

    def get_user_photos(self, obj):
        qs = obj.user_photos.all()
        return PhotoSerializer(qs, many=True, read_only=True).data

    def get_events_created(self, obj):
        qs = obj.event_author.all()
        from events.api.serializers import EventSerializer
        return EventSerializer(qs, many=True, read_only=True).data

    def get_events_visited(self, obj):
        qs = obj.event_member.all()
        from events.api.serializers import EventSerializer
        return EventSerializer(qs, many=True, read_only=True).data

    def get_user_rate(self, obj):
        qs = obj.user_rate.all()
        print(qs.values)
        return {'rate': 2}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class RateSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(
        required=True,
        validators=[rate_validator]
    )

    class Meta:
        model = Rate
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhoto
        fields = '__all__'





