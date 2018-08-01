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
            result = []
            result.append("email")
            result.append(self.request.GET["email"])
            if is_email_blacklisted(self.request.GET["email"]):
                result.append("YES")
            else:
                result.append("NO")
            context["results"].append(result)
        if "email_host" in self.request.GET:
            result = []
            result.append("email_host")
            result.append(self.request.GET["email_host"])
            if is_email_host_blacklisted(self.request.GET["email_host"]):
                result.append("YES")
            else:
                result.append("NO")
            context["results"].append(result)
        if "ip" in self.request.GET:
            result = []
            result.append("ip")
            result.append(self.request.GET["ip"])
            if is_ip_blacklisted(self.request.GET["ip"]):
                result.append("YES")
            else:
                result.append("NO")
            context["results"].append(result)

        return HttpResponse(self.template.render(context, request))
