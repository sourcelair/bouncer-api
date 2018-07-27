from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Blacklist")


def ip_request(request, ip):
    """
    Return YES if ip is blacklisted else NO
    """
    return HttpResponse("YO")
