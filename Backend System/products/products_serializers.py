from rest_framework import serializers
from .models import *

class Product_Category_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Category
        fields = '__all__'