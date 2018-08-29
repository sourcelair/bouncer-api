from rest_framework.response import Response
from rest_framework import views, viewsets
from collections import namedtuple
from rest_framework.decorators import action
from blacklist import models
import json
from blacklist.serializers import PostRequestSerializer
from blacklist.brain import (
    is_ip_blacklisted,
    is_email_blacklisted,
    is_email_host_blacklisted,
)


class GetRequestView(views.APIView):
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


class PostRequestViewSet(viewsets.ViewSet):
    @action(methods=["post"], detail=True)
    def add_entry(self, request, pk=None):
        data = json.loads(request.body)
        for entry in data:
            serializer = PostRequestSerializer(data=entry)
            if not serializer.is_valid():
                return Response(status=400)
            if serializer.validated_data["kind"] == "ip":
                ip_entry = models.IPEntry(entry_value=serializer.validated_data["value"])
                ip_entry.save()
            elif serializer.validated_data["kind"] == "email":
                email_entry = models.EmailEntry(entry_value=serializer.validated_data["value"])
                email_entry.save()
            elif serializer.validated_data["kind"] == "email_host":
                host_entry = models.EmailHostEntry(entry_value=serializer.validated_data["value"])
                host_entry.save()
        return Response(status=201)
