from rest_framework import serializers
from .models import WhitelistRequest

class WhitelistRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhitelistRequest
        fields = '__all__'
