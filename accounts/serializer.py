from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password')
        return data
    
    def validate_password(self,value):
        return make_password(value)