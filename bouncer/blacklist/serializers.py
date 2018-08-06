from rest_framework import serializers
from blacklist import models


class SingleResponseSerializer(serializers.Serializer):
    kind = serializers.CharField()
    value = serializers.CharField()
    result = serializers.BooleanField()


"""
class ResponseListSerializer(serializers.Serializer):
    responses = ResponseSerializer(many=True)"""


class ResponseSerializer(serializers.Serializer):
    response_list = serializers.ListField(
        child=serializers.DictField(child=SingleResponseSerializer())
    )
