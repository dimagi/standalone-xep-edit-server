# Create your views here.
from urllib2 import urlopen
from django.http import HttpResponse
from urllib import urlencode
def index(request):
    url = "http://192.168.7.107:8888" + request.get_full_path()[2:]
    return HttpResponse(urlopen(url).read())

