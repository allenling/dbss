#coding=utf8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

admin.autodiscover()

from dbss.views import IndexPage, DrivingPage, TagsPage, UsersPage, logout_user, ReUserWizard, FORMS,\
        CreateCard, WSearchView, TagCardPage, TagCardPageD

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$',IndexPage.as_view(), name = 'index'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^action/',include('dbss.action.urls',namespace='actionspace', app_name='action')),
    url(r'^driving/$',DrivingPage.as_view(), name = 'driving'),
    url(r'^tags/$',TagsPage.as_view(), name = 'tagspage'),
    url(r'^tags/(?P<tpk>\d+)/$',TagCardPage.as_view(), name = 'tagcard'),
    url(r'^tags/(?P<tpk>\d+)/driving/$',TagCardPageD.as_view(), name = 'tagcardd'),
    url(r'^users/$',UsersPage.as_view(), name = 'userspage'),
	url(r'^user/(?P<userpk>\d+)/',include('dbss.user_auth.urls',namespace='userspace', app_name='user_auth')),
	url(r'^card/(?P<pk>\d+)/',include('dbss.cardspace.urls',namespace='cardspace', app_name='cardspace')),
    url(r'^logout/$',logout_user, name='logout'),
    url(r'^register/$',ReUserWizard.as_view(FORMS), name = 'register'),	
    url(r'^createcard/$',login_required(CreateCard.as_view()), name = 'createcard'),	
    url(r'^search/$',WSearchView(), name = 'search'),	
)

urlpatterns+=patterns('',
	url(r'^captcha/',include('captcha.urls')),
)

urlpatterns+=patterns('',
	url(r'^avatar/',include('avatar.urls', namespace='avatar')),
)

urlpatterns+=patterns('',
	url(r'^ckeditor/',include('ckeditor.urls')),
)

urlpatterns+=patterns('',
	url(r'^account/',include('registration.backends.default.urls')),
)
urlpatterns +=patterns('',
    url(r'^api-auth/',include('rest_framework.urls', namespace = 'rest_framework')),
)
urlpatterns +=patterns('',
    url(r'^django-rq/',include('django_rq.urls',)),
)
