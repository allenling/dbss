#coding=utf8
import simplejson

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse, resolve

class MyappLoginRequired(object):

    def process_request(self, request):
        tmp = request.path
        app_name = resolve(tmp).app_name
        label_name = resolve(tmp).url_name
        if request.user.is_anonymous == True or request.user.is_authenticated() == False or request.user.is_active == False:
            if app_name in settings.LOGIN_REQUIRED_APP or label_name in settings.LOGIN_REQUIRED_NAME:
                if request.is_ajax():
                    rejson = simplejson.dumps({'type':'redirect'}, ensure_ascii = False)
                    return HttpResponse(rejson, content_type='application/json')
                reurl = reverse('auth_login')+'?next='+request.path
                return redirect(reurl)
