from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.template import loader
from blacklist import models
from collections import namedtuple
from blacklist.brain import (
    is_ip_blacklisted,
    is_email_blacklisted,
    is_email_host_blacklisted,
)


class RequestView(View):
    template = loader.get_template("blacklist/request.html")

    def get(self, request, *args, **kwargs):
        query = namedtuple("query", self.request.GET.keys())(**self.request.GET)
        context = {"results": []}
        if "email" in self.request.GET:
            for email in query.email:
                result = "NO"
                if is_email_blacklisted(email):
                    result = "YES"
                context["results"].append(["email", email, result])
        if "email_host" in self.request.GET:
            for host in query.email_host:
                result = "NO"
                if is_email_host_blacklisted(host):
                    result = "YES"
                context["results"].append(["email_host", host, result])
        if "ip" in self.request.GET:
            for ip in query.ip:
                result = "NO"
                if is_ip_blacklisted(ip):
                    result = "YES"
                context["results"].append(["ip", ip, result])

        return HttpResponse(self.template.render(context, request))
