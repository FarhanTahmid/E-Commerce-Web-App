from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = '__all__'

class TokenSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=Token
        fields = '__all__'