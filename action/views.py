#coding=utf-8
import simplejson

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import redirect

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from dbss.views import logout
from dbss.utils import deletefavlist, newfavlist

from dbss.cardspace.models import Card
from dbss.user_auth.models import UserFollow
from dbss.user_auth.models import MyUser as User

class ActionBaseMixin(object):

    def logon_required(self):
        if self.request.user.is_anonymous == True or self.request.user.is_authenticated() == False or self.request.user.is_active == False:
            if self.request.is_ajax():
                rejson = simplejson.dumps({'type':'redirect'}, ensure_ascii = False)
                return HttpResponse(rejson, content_type='application/json')
            reurl = reverse('auth_login')+'?next='+self.request.path
            return redirect(reurl)

    
class UserAction(ActionBaseMixin, APIView):

    render_classes = (JSONRenderer,)
    permission_classes = (permissions.IsAuthenticated,)
    notemplate_name = ''

    scontent = {'type':'success', 'msg':''}
    econtent = {'type':'error', 'msg':''}

    def get(self, request, *args,  **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        self.logon_required()
        tuid = simplejson.loads(request.DATA.get('tuid'))
        try:
            targetuser = User.objects.get(pk=tuid)
            self.action(targetuser)
        except Exception,e:
            content = self.econtent
        else:
            content = self.scontent
        return Response(content)

    @transaction.commit_on_success
    def action(self, targetuser):
        try:
            isf  = targetuser.isrefriend
        except AttributeError:
            targetuser.isrequestfriend(self.request.user)
            isf  = targetuser.isrefriend
        return isf

class RemoveConcern(UserAction):
    
    @transaction.commit_on_success
    def action(self, targetuser):
        isf = super(RemoveConcern,self).action(targetuser)
        if isf:
            self.request.user.removefriends(targetuser)
            self.request.user.requestconcern(targetuser)
            self.scontent["msg"]="remove success!"
            self.scontent["extra"]="bookmark"
        else:
            try:
                iscon = targetuser.rconcernme
            except AttributeError:
                targetuser.requestconcernme(self.request.user)
                iscon = targetuser.rconcernme
            if  iscon:
                targetuser.removerconcern(self.request.user)
                self.scontent["msg"]="remove success!"
                self.scontent["extra"]="plus"
            else:
                self.econtent['msg'] = u'you have not concern that user'
                raise UserFollow.DoesNotExist

class AddConcern(UserAction):
    
    @transaction.commit_on_success
    def action(self, targetuser):
        try:
            iscon = targetuser.rconcernme
        except AttributeError:
            targetuser.requestconcernme(self.request.user)
            iscon = targetuser.rconcernme
        if iscon:
            self.econtent['msg'] = u'you have concern that user '
            raise UserFollow.DoesNotExist
        else:
            try:
                addfriends = targetuser.meconcernr
            except AttributeError:
                targetuser.meconcernrequest(self.request.user)
                addfriends = targetuser.meconcernr
            if addfriends:
                targetuser.removeconcernr(self.request.user)
                targetuser.addfriends(self.request.user)
                self.scontent['msg']='add success!'
                self.scontent["extra"]="users"
            else:
                targetuser.requestconcern(self.request.user)
                self.scontent['msg']='add success!'
                self.scontent["extra"]="minus"

class BaseCardActionMixin(object):

    def get(self, request, *args, **kwargs):
        raise Http404
    
    def get_object(self, request):
       cid = request.DATA.get('cid')
       if cid != None:
           try:
               return  Card.objects.get(pk=cid)
           except Card.DoesNotExist:
                raise PermissionDenied
       else:
           raise PermissionDenied

class JoinCard(ActionBaseMixin, BaseCardActionMixin, APIView):

    permission_classes = (permissions.IsAuthenticated,)
    render_classes = (JSONRenderer,)
    allowclose = False

    @transaction.commit_on_success
    def post(self, request, *args,  **kwargs):
        self.logon_required()
        cardobj = self.get_object(request)
        try :
            cardobj.users.get(id = request.user.id)
            request.user.is_active = False
            request.user.save()
            logout(request)
            content = {'type':'error', 'msg': 'do not join again,you had joined this Card! and we will frozen you account.'}
        except User.DoesNotExist:
            cardobj.users.add(request.user)
            newfavlist(request.user.id, cardobj.id)
            content = {'type':'success', 'msg':'join success'}
        except Exception,e:
            content = {'type':'error', 'msg': str(e)}
        return Response(content)

class QuitCard(JoinCard):

    @transaction.commit_on_success
    def post(self, request, *args, **kwargs):
        try :
            cardobj = self.get_object(request)
            cardobj.users.get(pk = request.user.id)
            cardobj.users.remove(request.user)
            deletefavlist(request.user.id, cardobj.id)
            content = {'type':'success', 'msg':'quit success'}
        except User.DoesNotExist:
            request.user.is_active = False
            request.user.save()
            logout(request)
            content = {'type':'error', 'msg': 'do not  quit, you were not in this card! and we will frozen you account.'}
        except Exception,e:
            content = {'type':'error', 'msg': str(e)}
        return Response(content)
