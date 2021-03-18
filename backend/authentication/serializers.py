from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    username = serializers.CharField(max_length=64, min_length=4)
    first_name = serializers.CharField(max_length=64, min_length=2)
    last_name = serializers.CharField(max_length=64, min_length=2)
    email = serializers.EmailField(max_length=64, min_length=4)
    password = serializers.CharField(max_length=64, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email', '')).exists():
            raise serializers.ValidationError({'email': 'Email is already in use'})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)