#coding=utf8
from django.conf.urls import patterns,  url
from django.contrib import admin

admin.autodiscover()

from dbss.action.views import JoinCard, QuitCard
from dbss.action.views import AddConcern, RemoveConcern

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^removeconcern/$',RemoveConcern.as_view(),name='rfriend'),
    url(r'^addconcern/$',AddConcern.as_view(),name='afriend'),
    url(r'^joincard/$',JoinCard.as_view(), name = 'joincard'),	
    url(r'^quitcard/$',QuitCard.as_view(), name = 'quitcard'),	
)
