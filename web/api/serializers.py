from django.contrib.auth import authenticate
from rest_framework import serializers
from core.models import Faq, User, Block, Poll


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = ('title', 'description')


class BlockWrite(serializers.Serializer):
    user = serializers.CharField(max_length=128)
    permanent = serializers.BooleanField(default=False)
    warn = serializers.IntegerField(default=1, allow_null=True)

    def create(self, validated_data):
        return Block.objects.create(**validated_data)


class UserWrite(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    user_id_tg = serializers.IntegerField()
    warn = serializers.IntegerField(default=0, allow_null=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instace, validated_data):
        instace.username = validated_data.get('username', instace.username)
        instace.first_name = validated_data.get('first_name', instace.first_name)
        instace.last_name = validated_data.get('last_name', instace.last_name)
        instace.user_id_tg = validated_data.get('user_id_tg', instace.user_id_tg)
        instace.save()
        return instace


class UserWriteDetail(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    user_id_tg = serializers.IntegerField()
    warn = serializers.IntegerField()


class PollWrite(serializers.Serializer):
    keyboard_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    total_voted = serializers.IntegerField(default=1, allow_null=True)

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None:
            raise serializers.ValidationError(
                'Поле обязательно'
            )
        if password is None:
            raise serializers.ValidationError(
                'Поле обязательно'
            )
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'User is None'
            )
        return {
            'username': user.username,
            'token': user.token
        }

