# Create your views here.
from urllib2 import urlopen
from django.http import HttpResponse
from urllib import urlencode
from forwarder import config 

def index(request):
    url = "%s%s" % (config.FORWARDER_URL, request.get_full_path()[2:])
    return HttpResponse(urlopen(url).read())

