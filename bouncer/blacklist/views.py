from rest_framework.response import Response
from rest_framework import views
from collections import namedtuple
from blacklist.brain import (
    is_ip_blacklisted,
    is_email_blacklisted,
    is_email_host_blacklisted,
)


class RequestView(views.APIView):
    def get(self, request):
        result_list = []
        email_query = request.GET.getlist("email")
        for email in email_query:
            result = is_email_blacklisted(email)
            response = {"kind": "email", "value": email, "result": result}
            result_list.append(response)
        host_query = self.request.GET.getlist("email_host")
        for host in host_query:
            result = is_email_host_blacklisted(host)
            response = {"kind": "email_host", "value": host, "result": result}
            result_list.append(response)
        ip_query = self.request.GET.getlist("ip")
        for ip in ip_query:
            result = is_ip_blacklisted(ip)
            response = {"kind": "ip", "value": ip, "result": result}
            result_list.append(response)
        return Response(result_list)

    def get_extra_actions(cls):
        return []
