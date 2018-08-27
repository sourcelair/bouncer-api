from rest_framework import permissions


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
        for entry in request.body:
            if entry["kind"] == "ip":
                if not request.user.has_perm("blacklist.add_ipentry"):
                    return False
            elif entry["kind"] == "email":
                if not request.user.has_perm("blacklist.add_emailentry"):
                    return False
            elif entry["kind"] == "email_host":
                if not request.user.has_perm("blacklist.add_emailhostentry"):
                    return False
        return True
