from rest_framework import serializers
from .models import *

class AdminPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPositions
        fields = '__all__'
