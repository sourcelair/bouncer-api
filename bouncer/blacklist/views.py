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
        context = {"results": []}
        Row = namedtuple("Row", ["kind", "value", "result"])
        email_query = self.request.GET.getlist("email")
        for email in email_query:
            result = "NO"
            if is_email_blacklisted(email):
                result = "YES"
            row = Row("email", email, result)
            context["results"].append(row)
        host_query = self.request.GET.getlist("email_host")
        for host in host_query:
            result = "NO"
            if is_email_host_blacklisted(host):
                result = "YES"
            row = Row("email_host", host, result)
            context["results"].append(row)
        ip_query = self.request.GET.getlist("ip")
        for ip in ip_query:
            result = "NO"
            if is_ip_blacklisted(ip):
                result = "YES"
            row = Row("ip", ip, result)
            context["results"].append(row)

        return HttpResponse(self.template.render(context, request))
