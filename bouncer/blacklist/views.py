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


class IPRequestView(View):
    template = loader.get_template("blacklist/ip_request.html")

    def get(self, request, *args, **kwargs):
        context = {"request_list": []}
        if "email" in self.request.GET:
            context["request_list"].append("email")
            context["request_list"].append(self.request.GET["email"])
            if is_email_blacklisted(self.request.GET["email"]):
                context["request_list"].append("YES")
            else:
                context["request_list"].append("NO")
        if "email_host" in self.request.GET:
            context["request_list"].append("email_host")
            context["request_list"].append(self.request.GET["email_host"])
            if is_email_host_blacklisted(self.request.GET["email_host"]):
                context["request_list"].append("YES")
            else:
                context["request_list"].append("NO")
        if "ip" in self.request.GET:
            context["request_list"].append("ip")
            context["request_list"].append(self.request.GET["ip"])
            if is_ip_blacklisted(self.request.GET["ip"]):
                context["request_list"].append("YES")
            else:
                context["request_list"].append("NO")

        # print (context)
        return HttpResponse(self.template.render(context, request))
