from rest_framework import serializers
import ipaddress
import re


class PostRequestSerializer(serializers.Serializer):
    kind = serializers.ChoiceField(choices=["ip", "email", "email_host"])
    value = serializers.CharField(max_length=254)
    reason = serializers.CharField(allow_blank=True, default="")

    def validate(self, data):
        """
        Check that value is what kind is declared to be.
        """
        if data["kind"] == "ip":
            try:
                ipaddress.ip_address(data["value"])
            except ValueError:
                raise serializers.ValidationError("Value is not an IP address.")
        elif data["kind"] == "email" and not re.match(
            r"[\w!#$%&\'*+-/=?^_`{|}~.]+@[\w\.-]+", data["value"]
        ):
            raise serializers.ValidationError("Value is not an email.")
        return data
