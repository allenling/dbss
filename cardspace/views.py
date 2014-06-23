#coding=utf8
import re
import simplejson
import pickle
from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F,Q
from django.db import transaction
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit  import CreateView

import django_rq

from rest_framework.generics import ListAPIView

from redis_cache import get_redis_connection

from dbss.utils import MyPaginate, distr_object, updatefcard, send_message
from dbss.cardspace.serializers import UserSnapshoot, CinviteFriends, FcardSerializer
from dbss.cardspace.forms.cardspaceform import FCardNewForm
from dbss.cardspace.models import Card, Fcard

from dbss.user_auth.models import MyUser as User
from dbss.user_auth.views import InviteFriendsList

class BaseCardViewMixin(SingleObjectMixin):

    allowclose = True

    def get_object(self, queryset = Card.objects.all()):
        try:
            tmpcard =  super(BaseCardViewMixin, self).get_object(queryset)
            if tmpcard.isclose == True:
                if self.allowclose == False:
                    raise Card.DoesNotExist
            if tmpcard.property == 'Private':
                if tmpcard.private_card.preuser.filter(pk=self.request.user.id).exists() == False:
                    raise Card.DoesNotExist
            return tmpcard
        except Card.DoesNotExist:
            raise Http404


class CardInfo(BaseCardViewMixin, ListView):

    model = Card
    template_name = 'cardspace/cardinfo.html'
    context_object_name = 'card'
    paginate_by = 2
    endcard = F('id')
    mode = 'latest'
    order_item={'latest': '-pub_date', 'driving': '-score'}
    form_class = FCardNewForm
    show_rich = False
    fcard_id = 0


    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset = super(CardInfo, self).get_queryset())
        return super(CardInfo, self).get(request, *args, **kwargs)

    def get_queryset(self):
        a_queryset = self.object.maincard.filter(nextcard = self.endcard).order_by(self.order_item.get(self.mode))
        first_two = []
        other_f = None
        try:
            temp = a_queryset.get(carduser = self.object.carduser)
            if self.request.user.is_anonymous() == False and self.request.user.id == self.object.carduser.id:
                self.fcard_id = temp.id
            first_two.append(temp)
        except ObjectDoesNotExist:
            pass
        if self.request.user.is_anonymous() == False and self.request.user.id != self.object.carduser.id:
            try:
                tmp = a_queryset.get(carduser = self.request.user)
                self.fcard_id = tmp.id
                first_two.append(tmp)
            except ObjectDoesNotExist:
                pass
            other_f = a_queryset.exclude(Q(carduser = self.object.carduser)|Q(carduser = self.request.user))
        else:
            other_f = a_queryset.exclude(Q(carduser=self.object.carduser))
        first_two.extend(other_f)
        self.queryset = first_two
        return self.queryset

    def get_show_update(self):
        return self.request.user.is_anonymous() == False and self.object.users.filter(id = self.request.user.id).exists()

    def get_context_data(self, *args, **kwargs):
        context_data = super(CardInfo, self).get_context_data(*args, **kwargs)
        temp_page = MyPaginate(context_data['page_obj'].number, context_data['paginator'].num_pages)
        context_data['phead'] = temp_page.phead
        context_data['pageheadot'] = temp_page.pageheadot
        context_data['ptail'] = temp_page.ptail
        context_data['pagetaildot'] = temp_page.pagetaildot
        context_data['mode'] = self.mode
        context_data['updateform'] = self.form_class()
        context_data['show_rich'] = self.get_show_update()
        context_data['fcard_id'] = self.fcard_id
        return context_data


class CardInfoD(CardInfo):
    mode = 'driving'


class UserSnapList(BaseCardViewMixin, ListAPIView):

    paginate_by = 2
    paginate_by_param = 'page_c'
    serializer_class = UserSnapshoot
    model = User

    def get(self, request, *args, **kwargs):
        card = self.get_object()
        self.queryset = card.users.all()
        return super(UserSnapList, self).get(request, *args, **kwargs)


class CinviteFriendsList(BaseCardViewMixin, InviteFriendsList):

    serializer_class = CinviteFriends
    allowclose = False

    def get_serializer_context(self):
        context_data = super(CinviteFriendsList, self).get_serializer_context()
        context_data['pk'] = self.card_pk
        return context_data

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.users.get(id = request.user.id)
        except request.user.DoesNotExist:
            raise Http404

        self.card_pk = kwargs.get('pk')

        return super(CinviteFriendsList, self).get(request, *args, **kwargs)

class BlackList(BaseCardViewMixin, View):

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        pass

class WhiteList(BlackList, View):

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        pass

class UpdateFcard(BaseCardViewMixin, CreateView):

    model = Fcard
    form_class = FCardNewForm
    card_arg = 'card_pk'
    fcard_arg = 'fcard_pk'
    tmp_f = None
    mode_url = {'latest': 'cardspace:cardinfo', 'driving': 'cardspace:cardinfod'}
    f_object = None
    chain = None
    t_score = 0.1
    allowclose = False

    def get_object(self, queryset = None):
        c_object = super(UpdateFcard,self).get_object()
        try:
            if int(self.kwargs.get(self.fcard_arg)) != 0:
                self.f_object = Fcard.objects.get(pk = int(self.kwargs.get(self.fcard_arg)))
        except (Card.DoesNotExist, Fcard.DoesNotExist):
            raise Http404
        return c_object

    def get(self, request, *args, **kwargs):
        raise Http404


    def post(self, request, *args, **kwargs):
        try:
            mode = request.POST.get('currentmode')
        except:
            raise Http404
        if mode == None:
            raise Http404
        self.object = self.get_object()
        form_instance = self.form_class(request.POST)
        if form_instance.is_valid():
            up_fcard = self.get_new_fcard(self.request)
            tt = up_fcard.create_activity(verb = 'updatefcard')
            pickle_object = pickle.dumps(tt)
            redis_c = get_redis_connection('feed_storage')
            redis_c.lpush(self.request.user.id, pickle_object)
            if up_fcard.mcard.property == 'Public':
                redis_c.lpush(str(self.request.user.id)+settings.USER_PUBLIC_FEED, pickle_object)
            feed_queue = django_rq.get_queue('feed')
            updatefcard_queue = django_rq.get_queue('default')
            feed_list = Card.objects.raw('SELECT id, myuser_id FROM cardspace_card_users WHERE myuser_id <> %s and card_id =%s'%(self.request.user.id, up_fcard.mcard.id))
            feed_queue.enqueue(distr_object, tt, feed_list = [i.myuser_id for i in feed_list])
            updatefcard_queue.enqueue(updatefcard, up_fcard.id)
        return HttpResponseRedirect(reverse(self.mode_url.get(mode), kwargs={'pk': self.object.id}))


    @transaction.commit_on_success
    def get_new_fcard(self, request):
        tmp_new_f = Fcard(context = request.POST['context'], carduser = request.user, 
                         mcard = self.object, prevcard = self.f_object)
        tmp_new_f.save()
        if self.f_object != None:
            self.f_object.nextcard = tmp_new_f
            self.f_object.save()
            tmp_new_f.mfcard = self.f_object.mfcard
            tmp_new_f.graphic = self.f_object.graphic
        else:
            tmp_new_f.prevcard = tmp_new_f
            tmp_new_f.mfcard = tmp_new_f
        tmp_new_f.nextcard = tmp_new_f
        tmp_new_f.save()
        return tmp_new_f

class EditFcard(BaseCardViewMixin, View):
    
    model = Fcard
    form_class = FCardNewForm
    fcard_limit = F('id')
    template_name = 'cardspace/editfcard.html'

    def can_do(self,request, *args, **kwargs):
        self.object = self.get_object()
        self.fid = kwargs.get('user_pk')
        ist = str(self.fid) == str(request.user.id)
        if ist == False:
            raise Http404
        try:
            self.fcardobj = Fcard.objects.get(mcard = self.object, carduser__id = request.user.id, nextcard = self.fcard_limit) 
        except Fcard.DoesNotExist:
            raise Http404

    def get_context_data(self, *args, **kwargs):
        context_data ={}
        context_data['card'] = self.object
        context_data['fcardusername'] = self.request.user.get_full_name
        return context_data

    def get(self, request, *args, **kwargs):
        self.can_do(request, *args, **kwargs)
        context_data = self.get_context_data(*args, **kwargs)
        context_data['form'] = self.form_class({'context': self.fcardobj.context})
        return render(request,self.template_name, context_data)

    @transaction.commit_on_success
    def post(self, request, *args, **kwargs):
        self.can_do(request, *args, **kwargs)
        upform = self.form_class(request.POST)
        if upform.is_valid():
            self.fcardobj.context = upform.cleaned_data['context']
            self.fcardobj.save()
            return render(request, 'done.html', {'reurl': reverse('cardspace:cardinfo', kwargs={'pk': self.object.id }), 'content': 'edit success'})
        context_data = self.get_context_data(*args, **kwargs)
        context_data['form'] = upform
        return render(request,self.template_name, context_data)


class FCardInfo(BaseCardViewMixin, ListView):
    
    model  = Fcard
    paginate_by = 15
    template_name = 'cardspace/fcardinfo.html'

    def get_queryset(self):
        self.object = self.get_object()
        try:
            fcarduser = User.objects.get(pk=self.kwargs.get('user_pk'))
            self.fcarduser =fcarduser.get_full_name
            all_fcard = Fcard.objects.filter(mcard = self.object, carduser = fcarduser)
            if all_fcard.count() == 0:
                raise Fcard.DoesNotExist
            self.queryset = all_fcard
            return all_fcard
        except (Card.DoesNotExist, User.DoesNotExist, Fcard.DoesNotExist):
            raise Http404

    def get_context_data(self, *args, **kwargs):
        context_data = super(FCardInfo, self,).get_context_data(*args,**kwargs)
        context_data['card'] = self.object
        context_data['fcardusername'] = self.fcarduser
        return context_data

class InviteFriends(BaseCardViewMixin, View):

    template_name = 'cardspace/invitefriends.html'
    allowclose = False

    def inviteprocess(self, u_list):
        content = {}
        content['who_id'] = self.request.user.id
        if self.object.carduser == self.request.user:
            context = unicode('''<p >我创建了一个 {pro} 活动卡:<a href="{turl}">{ctitle}</a>, 快来加入我吧!</p>''')
        else:
            context = unicode('''<p >我发现了一个 a {pro} 活动卡:<a href="{turl}">{ctitle}</a>, 快来加入我吧!</p>''')
        self.objurl = reverse('cardspace:cardinfo', kwargs = {'pk':self.object.id})
        context = context.format(pro = self.object.property, turl = self.objurl, ctitle = self.object.getitle())
        content['context'] = context
        content['pub_date'] = datetime.now()
        content['status'] = 'Unread'
        content['action'] = 'Invite'
        content['showhtml'] = True
        feed_queue = django_rq.get_queue('feed')
        feed_queue.enqueue(send_message, content = content, ulist = u_list, action = content['action'], \
                           property = self.object.property, objid = self.object.id)

    def get(self, request,*args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.users.get(pk = request.user.id)
        except request.user.DoesNotExist:
            raise Http404
        return render(request, self.template_name, {'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.users.get(pk = request.user.id)
            userlist = self.request.POST.get('invited_people')
            inpattern = re.compile('^(\d+_){1,}$')
            if re.match(inpattern, userlist) is None:
                raise request.user.DoesNotExist
            split_list = [j for j in userlist.split('_') if j != ""]
            u_list =[i for i in self.request.user.friends.in_bulk(split_list)]
            self.inviteprocess(u_list)
        except request.user.DoesNotExist:
            raise Http404
        return HttpResponseRedirect(self.objurl)


class FuserGraphic(BaseCardViewMixin, View):

    model = Card

    def get(self, request, *args,  **kwargs):
        auth_card = self.get_object()
        graphic_r = get_redis_connection('graphic')
        allg = graphic_r.hgetall(str(auth_card.id) + '_' + kwargs.get('user_pk'))
        tmp = {}
        year_p = re.compile('^\d{4}$')
        for i in allg:
            if re.match(year_p, i):
                tmp.update({i:allg[i]})
        return HttpResponse(simplejson.dumps(tmp))

class FuserGraphicy(BaseCardViewMixin, View):

    model = Card

    def get(self, request, *args, **kwargs):

        auth_card = self.get_object()
        graphic_r = get_redis_connection('graphic')
        allg = graphic_r.hgetall(str(auth_card.id) + '_' + kwargs.get('user_pk'))
        tmp ={}
        month_p = re.compile('^'+kwargs.get('gyear')+'_\d{1,2}_c$')
        for i in allg:
            if re.match(month_p, i):
                tmp.update({i:allg[i]})
        return HttpResponse(simplejson.dumps(tmp))


class FuserGraphicm(BaseCardViewMixin, View):
    
    model = Card
    
    def get(self,request, *args, **kwargs):
        auth_card = self.get_object()
        graphic_r = get_redis_connection('graphic')
        allg = graphic_r.hgetall(str(auth_card.id) + '_' + kwargs.get('user_pk'))
        param = allg.get(kwargs.get('gyear')+'_'+kwargs.get('gmonth')+'_s')
        return HttpResponse(simplejson.dumps(param))


class FuserGraphicd(BaseCardViewMixin, View):

    model = Card

    def get(self, request, *args, **kwargs):
        auth_card = self.get_object()
        graphic_r = get_redis_connection('graphic')
        allg = graphic_r.hgetall(str(auth_card.id) + '_' + kwargs.get('user_pk'))
        param = allg.get(kwargs.get('gyear')+'_'+kwargs.get("gmonth")+'_d')
        if param:
            param = simplejson.loads(param)
        rparam = param.get(kwargs.get("gday")) if param else []
        return HttpResponse(simplejson.dumps(rparam))


class SearchFcardList(BaseCardViewMixin, ListAPIView):

    paginate_by = 2
    paginate_by_param = 'page_c'
    model = Fcard
    serializer_class = FcardSerializer

    def get_object(self, card_pk, user_pk):
        cardobj = super(SearchFcardList, self).get_object()
        fcardsobj = Fcard.objects.filter(mcard__id = cardobj.id, carduser__id = user_pk)
        return fcardsobj

    def get(self, request, *args, **kwargs):
        card_id, user_id = kwargs.get('card_pk'), kwargs.get('user_pk')
        fcards = self.get_object(card_pk = card_id, user_pk = user_id)
        fyear, fmonth, fday = kwargs.get('fyear'), kwargs.get('fmonth'), kwargs.get('fday')
        if fyear:
            if fmonth:
                if fday:
                    self.queryset = fcards.filter(pub_date__year = fyear, pub_date__month = fmonth, pub_date__day = fday)
                else:
                    self.queryset = fcards.filter(pub_date__year = fyear, pub_date__month = fmonth)
            else:
                self.queryset = fcards.filter(pub_date__year = fyear)
        else:
            raise Http404
        return super(SearchFcardList, self).get(request, *args, **kwargs)
