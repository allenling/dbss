#coding=utf8
import simplejson
import pickle

from django import forms
from django.conf import settings
from django.contrib.formtools.wizard.views import SessionWizardView
from django.http import Http404
from django.http import HttpResponseRedirect 
from django.views.generic import ListView
from django.views.generic.edit  import CreateView
from django.contrib.auth import logout
from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite
from django.db import transaction
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response

import django_rq
from redis_cache import get_redis_connection

from haystack.query import SearchQuerySet
from haystack.views import SearchView

from registration.models import RegistrationProfile

from dbss.utils import MyPaginate, distr_object,  newfavlist
from dbss.myform.registerform import ReUserForm1, ReUserForm3
from dbss.myform.searchform import SearchForm


from dbss.user_auth.models import MyUser as User
from dbss.user_auth.models import UserFollow

from dbss.cardspace.models import Card, CardTag, PrivateCardPreuser
from dbss.cardspace.forms.cardspaceform import CardNewForm


class IndexPage(ListView):
    model = Card
    template_name = 'base.html'
    context_object_name = 'cardobject'
    paginate_by = 20

    def get_queryset(self):
        return Card.objects.filter(property = 'Public').filter(isclose = False).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context_data = super(IndexPage, self).get_context_data(**kwargs)
        temp_page = MyPaginate(context_data['page_obj'].number, context_data['paginator'].num_pages)
        context_data['phead'] = temp_page.phead
        context_data['pageheadot'] = temp_page.pageheadot
        context_data['ptail'] = temp_page.ptail
        context_data['pagetaildot'] = temp_page.pagetaildot
        return context_data

class DrivingPage(IndexPage):
    template_name = 'driving.html'
    
    def get_queryset(self):
        return Card.objects.filter(property = 'Public').filter(isclose = False).order_by('-score')


class TagsPage(IndexPage):

    template_name = 'tags.html'
    model = CardTag
    paginate_by = 50
    context_object_name = 'tagobject'

    def get_queryset(self):
        return CardTag.objects.order_by('-allc')

class TagCardPage(IndexPage):

    template_name = 'tagcard.html'
    pattern = 'N'

    def get_queryset(self):
        self.queryset = self.tagobj.ctag.all()
        return self.queryset

    def get_context_data(self, **kwargs):
        context_data = super(TagCardPage, self).get_context_data(**kwargs)
        context_data['tagobj'] = self.tagobj
        context_data['pattern'] = self.pattern
        return context_data

    def get(self, request, *args, **kwargs):
        try:
           self.tagobj = CardTag.objects.get(pk=kwargs.get('tpk'))
        except CardTag.DoesNotExist:
            raise Http404
        return super(TagCardPage, self).get(request, *args, **kwargs)

class TagCardPageD(TagCardPage):

    pattern = 'D'

    def get_queryset(self):
        self.queryset = self.tagobj.ctag.order_by('-score')
        return self.queryset

class UsersPage(ListView):
    template_name = 'guys.html'
    model = User
    paginate_by = 10
    context_object_name = 'usersobject'

    def get_queryset(self):
        return User.objects.exclude(id = 1).order_by('-score')

    def getrequestfri(self, fobj):
		fobj.isrequestfriend(self.request.user)
		fobj.meconcernrequest(self.request.user)
		fobj.requestconcernme(self.request.user)

    def get_context_data(self, **kwargs):
        context_data = super(UsersPage, self).get_context_data(**kwargs)
        map(self.getrequestfri, context_data['object_list'])
        return context_data

def logout_user(request):
	logout(request)
	return HttpResponseRedirect(request.GET['next'])

TEMPLATES = {'base': 'register1.html',
             'captcha': 'register2.html',
            }


FORMS = [('base', ReUserForm1),
         ('captcha', ReUserForm3),
        ]

class ReUserWizard(SessionWizardView):

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def render_revalidation_failure(self, step, form, **kwargs):
        if step == 'captcha':
            if self.storage.get_step_data(step):
                done_responses = self.done(self.get_form_list(), **kwargs)
                self.storage.reset()
                return done_responses
        return super(ReUserWizard, self).render_revalidation_failure(step, form, **kwargs)

    def get_context_data(self, form, **kwargs):
        context_data = super(ReUserWizard, self).get_context_data(form = form, **kwargs)
        context_data['next'] = self.request.POST['next'] if 'next' in self.request.POST else self.request.GET['next'] if 'next' in self.request.GET else '/' 
        return context_data

    def done(self, form_list, **kwargs):
        base_data = self.storage.get_step_data('base')
        username = base_data.get('base-username')
        email = base_data.get('base-email')
        password = base_data.get('base-password')
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(self.request)
        RegistrationProfile.objects.create_inactive_user(username, email, password, site)
        return HttpResponseRedirect(reverse('registration_complete'))


class CreateCard(CreateView):

    model = Card
    form_class = CardNewForm
    template_name = 'createcard.html'
    tag_many = False
    follomeraw = 'SELECT id, fuser_id FROM user_auth_userfollow WHERE tuser_id = %s'
    friendsraw = 'SELECT id, to_myuser_id FROM user_auth_myuser_friends WHERE from_myuser_id = %s'

    @transaction.commit_on_success
    def new_card(self, form):
        tags_list = self.request.POST.get('tags').split(',')
        tmp_card = Card(title = form.cleaned_data['title'], context = form.cleaned_data['context'], property = form.cleaned_data['property'], carduser = self.request.user)
        tmp_card.save()
        tmp_card.users.add(self.request.user)
        for i in tags_list[:4]:
            tmp_tag = CardTag.objects.get_or_create(tag = i)
            tmp_tag = tmp_tag[0]
            tmp_tag.allc = tmp_tag.allc+1
            tmp_tag.save()
            tmp_card.tags.add(tmp_tag)
        tmp_card.save()
        if self.request.user.favlist == None or self.request.user.favlist == '' or self.request.user.favlist == 'null':
            t_f = {}
        else :
            t_f = self.request.user.favlist
            t_f = simplejson.loads(self.request.user.favlist)
        t_f.update({tmp_card.id:'All'})
        self.request.user.favlist = simplejson.dumps(t_f)
        self.request.user.save(update_fields=['favlist'])
        return tmp_card

    def processfeed(self, tmp_card, form, followers_list):
            #public card
            if form.cleaned_data.get('property') == 'Public':
                tt = tmp_card.create_activity(verb = 'createpubcard')
                rt = pickle.dumps(tt)
                redis_c = get_redis_connection('feed_storage')
                redis_c.lpush(self.request.user.id, rt)
                redis_c.lpush(str(self.request.user.id)+settings.USER_PUBLIC_FEED, rt) 
                feed_queue = django_rq.get_queue('feed')
                #friends_list = UserFollow.objects.raw(self.follomeraw%self.request.user.id)
                feed_queue.enqueue(distr_object, tt, feed_list = followers_list)
                targeturl = 'cardspace:cardinfo'
            #private card
            elif form.cleaned_data.get('property') == 'Private':
                tt = tmp_card.create_activity(verb = 'createpricard')
                rt = pickle.dumps(tt)
                redis_c = get_redis_connection('feed_storage')
                redis_c.lpush(self.request.user.id, rt)
                prcardpreuser = PrivateCardPreuser.objects.get_or_create(privatecard = tmp_card)
                prcardpreuser[0].preuser.add(self.request.user)
                targeturl = 'cardspace:invitefriends'
            return targeturl


    def form_valid(self, form):
        
        try:
            tags_list = self.request.POST.get('tags').split(',')
            if  ' ' in tags_list or len(tags_list) > 4:
                form.errors['tags'] = u'tags_list should be a least one, no one should be empty!'
                raise forms.ValidationError(u'tags_list should be a least one, no one should be empty!')
            tmp_card = self.new_card(form)
            newfavlist(self.request.user.id, tmp_card.id)
            followers_list = [i.fuser_id for i in UserFollow.objects.raw(self.follomeraw%self.request.user.id)]
            friends_list = [j.to_myuser_id for j in User.objects.raw(self.friendsraw%self.request.user.id)]
            followers_list.extend(friends_list)
            targeturl = self.processfeed(tmp_card, form, followers_list)
            return HttpResponseRedirect(reverse(targeturl, kwargs={'pk': tmp_card.id}))
        except Exception, e:
            return super(CreateCard, self).form_invalid(form)

class WSearchView(SearchView):

    results_per_page = 1
    model_map_int = {
        '123': {'model': 'cardspace.card', 'template_name':'search/search.html'},
        '456': {'model': 'cardspace.cardtag', 'template_name': 'search/searchtag.html'},
        '789': {'model': 'user_auth.myuser', 'template_name': 'search/searchuser.html'},
    }

    def build_form(self, form_kwargs = None):
        self.form_class = SearchForm
        new_request_get = self.request.GET.copy()
        kwargs = {}
        new_request_get.setlist('models',new_request_get.getlist('m'))

        models_num = new_request_get.getlist('models')
        if len(models_num) > 1:
            raise Http404
        if len(models_num) == 0:
            models_num.append('123')

        if len(models_num) == 1 and models_num[0] == '123':
            kwargs['searchqueryset'] = SearchQuerySet().filter(property = 'Public')
        try:
            tmp = [self.model_map_int.get(i).get('model') for i in models_num ]
        except AttributeError:
            raise Http404
        self.template = self.model_map_int.get(models_num[0]).get('template_name')

        kwargs['load_all'] = self.load_all
        new_request_get.setlist('models', tmp)
        if form_kwargs is not None:
            kwargs.update(form_kwargs)

        return self.form_class(new_request_get, **kwargs)

    def create_response(self):
        (paginator ,page) = self.build_page()
        context_data = {
            'query':self.query,
            'form':self.form,
            'page':page,
            'paginator':paginator,
            'suggestion':None,
        }
        temp_page = MyPaginate(page.number, paginator.num_pages)
        context_data['phead'] = temp_page.phead
        context_data['pageheadot'] = temp_page.pageheadot
        context_data['ptail'] = temp_page.ptail
        context_data['pagetaildot'] = temp_page.pagetaildot
        return render_to_response(self.template, context_data, context_instance=self.context_class(self.request))

def test(request):
    return render(request, template_name = 'done.html')
