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
        query = dict(self.request.GET.lists())
        context = {"request_list": []}
        if "email" in query:
            while query["email"] != []:
                context["request_list"].append("email")
                context["request_list"].append(query["email"][0])
                if is_email_blacklisted(query["email"][0]):
                    context["request_list"].append("YES")
                else:
                    context["request_list"].append("NO")
                query["email"].remove(query["email"][0])
        if "email_host" in query:
            while query["email_host"] != []:
                context["request_list"].append("email_host")
                context["request_list"].append(query["email_host"][0])
                if is_email_host_blacklisted(query["email_host"][0]):
                    context["request_list"].append("YES")
                else:
                    context["request_list"].append("NO")
                query["email_host"].remove(query["email_host"][0])
        if "ip" in query:
            while query["ip"] != []:
                context["request_list"].append("ip")
                context["request_list"].append(query["ip"][0])
                if is_ip_blacklisted(query["ip"][0]):
                    context["request_list"].append("YES")
                else:
                    context["request_list"].append("NO")
                query["ip"].remove(query["ip"][0])

        return HttpResponse(self.template.render(context, request))
