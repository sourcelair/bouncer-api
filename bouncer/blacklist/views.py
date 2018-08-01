from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.template import loader
from blacklist import models
from blacklist.brain import (
    is_ip_blacklisted,
    is_email_blacklisted,
    is_email_host_blacklisted,
)


class RequestView(View):
    template = loader.get_template("blacklist/ip_request.html")

    def get(self, request, *args, **kwargs):
        context = {"results": []}
        if "email" in self.request.GET:
            result = "NO"
            if is_email_blacklisted(self.request.GET["email"]):
                result = "YES"
            context["results"].append(["email", self.request.GET["email"], result])
        if "email_host" in self.request.GET:
            result = "NO"
            if is_email_host_blacklisted(self.request.GET["email_host"]):
                result = "YES"
            context["results"].append(
                ["email_host", self.request.GET["email_host"], result]
            )
        if "ip" in self.request.GET:
            result = "NO"
            if is_ip_blacklisted(self.request.GET["ip"]):
                result = "YES"
            context["results"].append(["ip", self.request.GET["ip"], result])

        return HttpResponse(self.template.render(context, request))
