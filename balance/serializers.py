from .models import Balance
from rest_framework import serializers

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['user','balance']