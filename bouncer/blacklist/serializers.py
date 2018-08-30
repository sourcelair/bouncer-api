from rest_framework import serializers
import ipaddress
import re


class BlacklistResourceSerializer(serializers.Serializer):
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
        elif data["kind"] == "email_host":
            if len(data["value"]) > 255:
                raise serializers.ValidationError("Value is not an email host.")
            if data["value"][-1] == ".":
                data["value"] = data["value"][:-1]
            allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
            if not all(allowed.match(x) for x in data["value"].split(".")):
                raise serializers.ValidationError("Value is not an email host.")
        return data
