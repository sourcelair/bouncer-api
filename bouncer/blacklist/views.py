from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from blacklist import models
from blacklist.brain import (
    is_ip_blacklisted,
    is_email_blacklisted,
    is_email_host_blacklisted,
)


class IPRequestView(View):
    def get(self, request, *args, **kwargs):
        if is_ip_blacklisted(request.GET["ip"]):
            return HttpResponse("YES")
        return HttpResponse("NO")
