from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=20, style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(max_length=20, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'pesel', 'email', 'password', 'password2')
        extra_kwargs = {'password': {
            'write_only': True
        }}

    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords not match'})
        if CustomUser.check_pesel_duplicates(validated_data['pesel']):
            print('elo')
            raise serializers.ValidationError({'pesel': 'User with this pesel already registered'})
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user
