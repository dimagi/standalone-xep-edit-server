from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
from django.core.urlresolvers import reverse

from .models import EditSession, BadSessionKey
from .utils import post_multipart

import json

@csrf_exempt
@require_POST
def initiate(request):
    session_key = request.POST['session_key']
    edit_session = EditSession(
        key = session_key,
        callback = request.POST['callback'],
        xform = request.FILES['xform'].read(),
    )
    edit_session.gentoken()
    edit_session.save()
    return HttpResponseRedirect("%s%s" % (settings.URL_BASE, reverse('xep_edit_server.views.start', args=[edit_session.token])))
    
@require_GET
def start(request, token):
    edit_session = EditSession.get_by_token(token)
    
    response = HttpResponseRedirect(settings.XEP_EDITOR.format(token=edit_session.token, status=""))
    edit_session.set_cookie(response)
    return response
    
@require_GET
def get_xform(request, token):
    try:
        edit_session = EditSession.safe_get(token, request)
        return HttpResponse(edit_session.xform)
    except BadSessionKey:
        return HttpResponseForbidden()

@csrf_exempt    
@require_POST   
def save(request):
    try:
        token = request.POST['token']
        cont = request.POST['continue']
        edit_session = EditSession.safe_get(token, request)
    except BadSessionKey:
        return HttpResponseForbidden()
        
    xform = request.FILES.get('xform', '')
    if xform:
        xform = xform.read()
    else:
        xform = request.POST['xform']
    
    edit_session.xform = xform
    edit_session.save()

    try:
        response = post_multipart(edit_session.callback, {
            'session_key': edit_session.key,
            'continue': cont,
        }.items(), [
            ('xform', 'xform.xml', xform)
        ])
        r = json.loads(response.content)
    except:
        r = {"continue": True, "status": "failed", "session_key": None, "callback": None}


    if r["continue"]:
        response = HttpResponseRedirect(settings.XEP_EDITOR.format(token=token, status=r['status']))
        if r['session_key']:
            edit_session.delete_cookie(response)
            edit_session.key = r['session_key']
            edit_session.save()
            edit_session.set_cookie(response)
    else:
        response = HttpResponseRedirect(r['callback'])
        edit_session.delete_cookie(response)
        edit_session.active = False
        edit_session.save()
    
    return response