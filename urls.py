from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^xep/', include('xep_edit_server.urls')),
    (r'^FormDesigner.html', 'example_editor.views.index'),
    (r'^f/', 'forwarder.views.index'),
)
