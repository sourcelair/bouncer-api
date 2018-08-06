from rest_framework import serializers
from blacklist import models

class ResponseSerializer(serializers.Serializer):
    kind = serializers.CharField()
    value = serializers.CharField()
    result = serializers.BooleanField()