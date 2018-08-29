from rest_framework import permissions
from blacklist.serializers import PostRequestSerializer
import json


class GetRequestViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if "ip" in request.GET:
            if not request.user.has_perm("blacklist.view_ipentry"):
                return False
        if "email" in request.GET:
            if not request.user.has_perm("blacklist.view_emailentry"):
                return False
        if "email_host" in request.GET:
            if not request.user.has_perm("blacklist.view_emailhostentry"):
                return False
        return True


class PostRequestViewSetPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            return True
        data = json.loads(request.body)
        for entry in data:
            serializer = PostRequestSerializer(data=entry)
            if serializer.is_valid():
                if serializer.validated_data["kind"] == "ip":
                    if not request.user.has_perm("blacklist.add_ipentry"):
                        return False
                elif serializer.validated_data["kind"] == "email":
                    if not request.user.has_perm("blacklist.add_emailentry"):
                        return False
                elif serializer.validated_data["kind"] == "email_host":
                    if not request.user.has_perm("blacklist.add_emailhostentry"):
                        return False
        return True
