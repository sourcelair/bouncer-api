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
        Row = namedtuple('Row', ['kind', 'value', 'result'])
        if "email" in self.request.GET:
            for email in query.email:
                result = "NO"
                if is_email_blacklisted(email):
                    result = "YES"
                row = Row('email', email, result)
                context["results"].append(row)
        if "email_host" in self.request.GET:
            for host in query.email_host:
                result = "NO"
                if is_email_host_blacklisted(host):
                    result = "YES"
                row = Row('email_host', host, result)
                context["results"].append(row)
        if "ip" in self.request.GET:
            for ip in query.ip:
                result = "NO"
                if is_ip_blacklisted(ip):
                    result = "YES"
                row = Row('ip', ip, result)
                context["results"].append(row)

        return HttpResponse(self.template.render(context, request))
