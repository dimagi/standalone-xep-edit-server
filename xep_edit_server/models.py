from django.db import models
from couchdbkit.ext.django.schema import *
import hashlib, random

class BadSessionKey(Exception):
    pass

class EditSession(Document):
    key = StringProperty()
    callback = StringProperty()
    xform = StringProperty()
    token = StringProperty()
    active = BooleanProperty(default=True)
    
    def _cookie_name(self):
        return str('session_key_%s' % self.key[:5])
    
    @classmethod
    def get_by_token(cls, token):
        return cls.view('xep_edit_server/sessions', key=token).one()
    @classmethod
    def safe_get(cls, token, request):
        edit_session = cls.get_by_token(token)
        if not edit_session.key == request.COOKIES[edit_session._cookie_name()]:
            raise BadSessionKey()
        else:
            return edit_session
            
    def set_cookie(self, response):
        response.set_cookie(self._cookie_name(), self.key)
        
    def delete_cookie(self, response):
        response.delete_cookie(self._cookie_name())
        
    def gentoken(self):
        self.token = hex(random.getrandbits(160))[2:-1]