from django.http import JsonResponse
from rest_framework import views
from collections import namedtuple
from blacklist.serializers import ResponseSerializer
from blacklist.brain import (
    is_ip_blacklisted,
    is_email_blacklisted,
    is_email_host_blacklisted,
)


class RequestView(views.APIView):
    def get(self, request):
        response_list = []
        email_query = request.GET.getlist("email")
        for email in email_query:
            result = False
            if is_email_blacklisted(email):
                result = True
            response = {"kind": "email", "value": email, "result": result}
            response_list.append(response)
        host_query = self.request.GET.getlist("email_host")
        for host in host_query:
            result = False
            if is_email_host_blacklisted(host):
                result = True
            response = {"kind": "email_host", "value": host, "result": result}
            response_list.append(response)
        ip_query = self.request.GET.getlist("ip")
        for ip in ip_query:
            result = False
            if is_ip_blacklisted(ip):
                result = True
            response = {"kind": "ip", "value": ip, "result": result}
            response_list.append(response)
        serializer = ResponseSerializer(response_list)
        return JsonResponse(serializer.data)

    @classmethod
    def get_extra_actions(cls):
        return []
