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

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )
    password = serializers.CharField(min_length=6)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    class Meta:
        model = CustomUser
        lookup_field = 'username'
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'avatar', 'date_of_birth')
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }


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





