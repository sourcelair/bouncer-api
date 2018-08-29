from rest_framework import permissions


class ViewPermission(permissions.BasePermission):
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
