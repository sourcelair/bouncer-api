from rest_framework import serializers

class PostRequestSerializer(serializers.Serializer):
    kind = serializers.CharField(max_length=11)
    value = serializers.CharField(max_length=254)