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
    template = loader.get_template("blacklist/request.html")

    def get(self, request, *args, **kwargs):
        query = dict(self.request.GET.lists())
        context = {"results": []}
        if "email" in self.request.GET:
            while query["email"] != []:
                result = "NO"
                if is_email_blacklisted(query["email"][0]):
                    result = "YES"
                context["results"].append(["email", query["email"][0], result])
                query["email"].remove(query["email"][0])
        if "email_host" in self.request.GET:
            while query["email_host"] != []:
                result = "NO"
                if is_email_host_blacklisted(query["email_host"][0]):
                    result = "YES"
                context["results"].append(
                    ["email_host", query["email_host"][0], result]
                )
                query["email_host"].remove(query["email_host"][0])
        if "ip" in self.request.GET:
            while query["ip"] != []:
                result = "NO"
                if is_ip_blacklisted(query["ip"][0]):
                    result = "YES"
                context["results"].append(["ip", query["ip"][0], result])
                query["ip"].remove(query["ip"][0])

        return HttpResponse(self.template.render(context, request))
