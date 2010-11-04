from django.conf.urls.defaults import *

urlpatterns = patterns('xep_edit_server.views',
    (r'^initiate/', 'initiate'),
    (r'^start/(?P<token>\w+)/', 'start'),
    (r'^xform/(?P<token>\w+)/', 'get_xform'),
    (r'^save/', 'save')
)