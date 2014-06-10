#coding=utf8
import pickle
from datetime import datetime
import simplejson

from django.conf import settings
from django.contrib.auth.views import password_change
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView, View

from avatar.views import add

from rest_framework import permissions
from rest_framework.generics import ListAPIView

import django_rq
from redis_cache import get_redis_connection

from dbss.utils import MyPaginate, send_message

from dbss.cardspace.models import Card

from dbss.user_auth.models import MyUser as User
from dbss.user_auth.models import UserFollow
from dbss.user_auth.forms.smessageform import SmessageForm
from dbss.user_auth.serializers import InviteFriends


class BaseUserMixin(object):

    isowner = False
    anonyauth = False

    def getisowner(self, request, kwargs):
        uid = kwargs.get('userpk')
        try:
            rquser = User.objects.get(pk=int(uid))
        except User.DoesNotExist:
            raise Http404
        upk = int(rquser.id)
        self.rquser = rquser
        if request.user.is_anonymous() == False and \
           request.user.is_authenticated():
            if request.user.id == upk:
                self.isowner = True
            else:
                try:
                    self.template_name = self.notemplate_name
                except AttributeError:
                    raise Http404
        else:
            try:
                self.template_name = self.notemplate_name
                self.anonyauth = True
            except AttributeError:
                raise Http404


class FeedPage(BaseUserMixin, ListView):

    template_name = 'user_auth/index.html'
    model = Card
    paginate_by = 30
    context_object_name = 'object'
    notemplate_name = 'user_auth/notindex.html'

    def get_queryset(self):
        redis_c = get_redis_connection('feed_storage')
        user_feed = []
        if self.isowner:
            tarredis = redis_c.lrange(str(self.rquser.id), 0, 1300)
        else:
            tarredis = redis_c.lrange(str(self.rquser.id) + \
                                      settings.USER_PUBLIC_FEED, 0, 1300)
        for i in tarredis:
            j = pickle.loads(i)
            j.set_real_user()
            user_feed.append(j)
        return user_feed

    def top_super_context(self, **kwargs):
        return super(FeedPage, self).get_context_data(**kwargs)

    def get_context_data(self, **kwargs):
        context_data = self.top_super_context(**kwargs)
        temp_page = MyPaginate(context_data['page_obj'].number, \
                               context_data['paginator'].num_pages)
        context_data['phead'] = temp_page.phead
        context_data['pageheadot'] = temp_page.pageheadot
        context_data['ptail'] = temp_page.ptail
        context_data['pagetaildot'] = temp_page.pagetaildot
        context_data['rquser'] = self.rquser
        context_data['isowner'] = self.isowner
        context_data['anonyauth'] = self.anonyauth
        if self.isowner == False:
            self.rquser.isrequestfriend(self.request.user)
            self.rquser.meconcernrequest(self.request.user)
            self.rquser.requestconcernme(self.request.user)
        return context_data

    def get(self, request, *args, **kwargs):
        self.getisowner(request, kwargs)
        return super(FeedPage, self).get(request, *args, **kwargs)


class MessagePage(BaseUserMixin, ListView):


    template_name = 'user_auth/message.html'
    model = Card
    paginate_by = 15
    context_object_name = 'object'
    sview = True
    msg_redis = get_redis_connection('message')

    def get_queryset(self):
        self.queryset = self.msg_redis.zrevrange(str(self.request.user.id), 0,\
                                                 -1)
        return self.queryset

    def top_super_context(self, **kwargs):
        return super(MessagePage, self).get_context_data(**kwargs)

    def load_msg(self, context_data):
        contacts = [str(self.request.user.id)+'_' + str(i) for i in context_data['object']]
        context_data['object'] = [simplejson.loads(self.msg_redis.lrange(j, 0, 0)[0]) for j in contacts]

    def get_context_data(self, **kwargs):
        context_data = self.top_super_context(**kwargs)
        temp_page = MyPaginate(context_data['page_obj'].number, context_data['paginator'].num_pages)
        context_data['phead'] = temp_page.phead
        context_data['pageheadot'] = temp_page.pageheadot
        context_data['ptail'] = temp_page.ptail
        context_data['pagetaildot'] = temp_page.pagetaildot
        context_data['rquser'] = self.rquser
        context_data['sview'] = self.sview
        context_data['anonyauth'] = self.anonyauth
        self.load_msg(context_data)
        return context_data

    def get(self, request, *args, **kwargs):
        self.getisowner(request, kwargs)
        return super(MessagePage, self).get(request, *args, **kwargs)

class GetMessage(MessagePage):

    paginate_by = 10
    paginate_by_param = 'page_c'
    sview = False
    template_name = 'user_auth/getmessage.html'

    def get_queryset(self):
        try:
            m = User.objects.get(pk = self.mpk)
        except User.DoesNotExist:
            raise Http404
        #set msg read
        first_msg = self.msg_redis.lpop(str(self.request.user.id)+ '_' + self.mpk)
        if first_msg != None:
            tmp = simplejson.loads(first_msg)
            tmp['status'] = 'read'
            self.msg_redis.lpush(str(self.request.user.id) + '_' + self.mpk, simplejson.dumps(tmp))
        self.queryset = self.msg_redis.lrange(str(self.request.user.id)+'_'+self.mpk, 0 , -1)
        self.targetuser = m
        #reduce user unread msg count
        if int(self.msg_redis.get('unread_' + str(self.request.user.id)) > 0):
            self.msg_redis.decr('unread_'+str(self.request.user.id))
        return self.queryset

    def load_msg(self, context_data):
        context_data['object'] = [simplejson.loads(i) for i in context_data['object']]

    def get_context_data(self, **kwargs):
        context_data = super(GetMessage, self).get_context_data(**kwargs)
        context_data['targetuser'] = self.targetuser
        return context_data

    def get(self, request, *args, **kwargs):
        self.getisowner(request, kwargs)
        self.mpk = kwargs.get('mpk')
        contacts = self.msg_redis.zrange(self.request.user.id, 0, -1)
        if self.mpk not in contacts:
            raise Http404
        return super(GetMessage, self).get(request, *args, **kwargs)

class SendMessage(BaseUserMixin, View):

    model = Card
    form_class = SmessageForm
    template_name = 'user_auth/smessage.html'
    object = None

    def validate_data(self, towhostr, context):
        form = self.form_class(self.request.POST)
        er = False
        towhonull = u'发送人不能为空'
        if towhostr == '':
            form.errors['towho'] = towhonull
            er = True
        if form.errors['towho'] != towhonull:
            form.errors['towho'] = u''
        if  len(context) <= 0:
            form.errors['context'] = u'内容不能为空'
            er = True
        elif len(context) > 300:
            form.errors['context'] = u'内容不能超过300个字符'
            er = True
        return er,form

    def processmessage(self, request, towholist, context):
        content = {}
        content['who_id'] = request.user.id
        content['who_username'] = request.user.get_full_name
        content['context'] = context
        content['pub_date'] = datetime.now().__str__()[:19]
        content['showhtml'] = False
        feed_queue = django_rq.get_queue('msgrq')
        feed_queue.enqueue(send_message, content = content, ulist = towholist, action = 'Send', \
                           property = 'Public')


    def post(self, request, *args, **kwargs):
        self.getisowner(request, kwargs)
        if self.isowner == False:
            raise Http404
        towhostr = request.POST['towho']
        context = request.POST['context']
        vadata, form = self.validate_data(towhostr, context)
        if vadata:
            return render(request, 'user_auth/smessage.html', {'form': form, 'rquser': self.rquser})
        towholist = towhostr.split(',')
        self.processmessage(request, towholist, context)
        return render(request, 'done.html', {'reurl': reverse('user_auth:mymessage', kwargs={'userpk': request.user.id }), 'content': 'send success'})


    def get_context_data(self, **kwargs):
        context_data = super(SendMessage, self).get_context_data(**kwargs)
        context_data['rquser'] = self.rquser
        return context_data

    def get(self, request, *args, **kwargs):
        self.getisowner(request, kwargs)
        return render(request, 'user_auth/smessage.html', {'form': self.form_class(), 'rquser': self.rquser})
    

class InviteFriendsList(BaseUserMixin, ListAPIView):

    paginate_by = 15
    paginate_by_param = 'page_c'
    model = User
    serializer_class = InviteFriends

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        self.getisowner(request, kwargs)
        if self.isowner == False:
            raise Http404
        self.queryset = request.user.friends.all()
        return super(InviteFriendsList, self).get(request, *args, **kwargs)

class PrivatePage(FeedPage):

    template_name = 'user_auth/private.html'
    model = Card
    paginate_by = 30
    context_object_name = 'object'

    def get_queryset(self):
        allpr = self.request.user.follower.filter(property = 'Private').filter(isclose = False).order_by('-pub_date')
        return allpr

    def get(self, request, *args, **kwargs):
        self.getisowner(request, kwargs)
        return super(FeedPage, self).get(request, *args, **kwargs)


class PublicPage(FeedPage):

    template_name = 'user_auth/public.html'
    model = Card
    paginate_by = 30
    context_object_name = 'object'
    notemplate_name = 'user_auth/notpublic.html'

    def get_queryset(self):
        allpc = self.rquser.follower.filter(property = 'Public').filter(isclose = False).order_by('-pub_date')
        return allpc

class FriendsPage(FeedPage):

    template_name = 'user_auth/friends.html'
    notemplate_name = 'user_auth/notfriends.html'

    def get_queryset(self):
        self.queryset = self.rquser.friends.prefetch_related('friends').all()
        return self.queryset

    def getrequestfri(self, fobj):
		fobj.isrequestfriend(self.request.user)
		fobj.meconcernrequest(self.request.user)
		fobj.requestconcernme(self.request.user)

    def get_context_data(self, **kwargs):
        context_data = super(FriendsPage, self).get_context_data(**kwargs)
        map(self.getrequestfri, context_data['object'])
        return context_data

class ConcernPage(FriendsPage):

    template_name = 'user_auth/concerns.html'
    notemplate_name = 'user_auth/notconcerns.html'

    def get_queryset(self):
        self.queryset = UserFollow.objects.prefetch_related('tuser__friends').filter(fuser = self.rquser)
        return self.queryset

    def getrequestfri(self, fobj):
		fobj.tuser.isrequestfriend(self.request.user)
		fobj.tuser.meconcernrequest(self.request.user)
		fobj.tuser.requestconcernme(self.request.user)

class ConcernmePage(ConcernPage):

    template_name = 'user_auth/concernmes.html'
    notemplate_name = 'user_auth/notconcernmes.html'

    def getrequestfri(self, fobj):
		fobj.fuser.isrequestfriend(self.request.user)
		fobj.fuser.meconcernrequest(self.request.user)
		fobj.fuser.requestconcernme(self.request.user)
    
    def get_queryset(self):
        self.queryset = UserFollow.objects.prefetch_related('fuser__friends').filter(tuser = self.rquser)
        return self.queryset


class EditProfile(BaseUserMixin, TemplateView):

    template_name = 'user_auth/editprofile.html'
    remind = None

    def get(self, request, *args, **kwargs):
        self.getisowner(request, kwargs)
        edit_ref = request.META.get('HTTP_REFERER')
        if edit_ref != None:
            if 'changepwd' in edit_ref:
                self.remind = 'change pwd success!'
            elif 'changeavatar' in edit_ref:
                self.remind = 'change your avatar success'
        return super(EditProfile, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EditProfile, self).get_context_data(**kwargs)
        context['rquser'] = self.rquser
        context['remind'] = self.remind
        return context

class ChangeAvatar(EditProfile):

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        self.getisowner(request, kwargs)
        request.META['HTTP_REFERER']=request.path
        return add(request=request, extra_context={'rquser': self.rquser, 'remind': 'update avatar error!'}, \
                   next_override = reverse('user_auth:useredit', kwargs={'userpk': request.user.id}),\
                   template_name = 'user_auth/editprofile.html')


class ChangePwd(EditProfile):

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        self.getisowner(request, kwargs)
        return password_change(request=request, template_name = 'user_auth/editprofile.html', \
                               post_change_redirect=reverse('user_auth:useredit', kwargs={'userpk': request.user.id}),\
                               extra_context = {'rquser': self.rquser, 'pwd': True})
