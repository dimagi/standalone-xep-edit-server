from django.conf import settings

FORWARDER_URL = getattr(settings, "FORWARDER_URL", "http://localhost:8012")
