from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )
    password = serializers.CharField(min_length=6)

    date_of_birth = serializers.CharField(max_length=20)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'date_of_birth')





