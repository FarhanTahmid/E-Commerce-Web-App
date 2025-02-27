from rest_framework import serializers
from .models import *
from e_commerce_app import settings

class Account_Serialier(serializers.ModelSerializer):

    class Meta:
        model = Accounts
        fields = [
            'email',
            'username',
            'phone_no'
        ]

class Notification_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'

class NotificationTo_Serializer(serializers.ModelSerializer):

    to = Account_Serialier(read_only=True)
    notification = Notification_Serializer(read_only=True)

    class Meta:
        model = NotificationTo
        fields= '__all__'