#coding=utf8
from django.conf.urls import patterns, url

from dbss.user_auth.views import FeedPage, MessagePage, GetMessage, SendMessage, InviteFriendsList, PrivatePage,\
        PublicPage, FriendsPage, ConcernPage, ConcernmePage, RemoveConcern, AddConcern, EditProfile, ChangeAvatar, ChangePwd

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$',FeedPage.as_view(),name='index'),
    url(r'^edit/',EditProfile.as_view(),name='useredit'),
    url(r'^changeavatar/',ChangeAvatar.as_view(),name='cavatar'),
    url(r'^changepwd/',ChangePwd.as_view(),name='cpwd'),
    url(r'^mypricard/$',PrivatePage.as_view(),name='myprivate'),
    url(r'^mypubcard/$',PublicPage.as_view(),name='mypublic'),
    url(r'^mymessage/$',MessagePage.as_view(),name='mymessage'),
    url(r'^mymessage/(?P<mpk>\d+)/$',GetMessage.as_view(),name='getmessage'),
    url(r'^smessage/$',SendMessage.as_view(),name='smessage'),
    url(r'^invitefriendlist/$',InviteFriendsList.as_view(),name='invitefriendlist'),
    url(r'^friends/$',FriendsPage.as_view(),name='myfriends'),
    url(r'^concerns/$',ConcernPage.as_view(),name='myconcerns'),
    url(r'^concernsm/$',ConcernmePage.as_view(),name='concernsme'),
    url(r'^removeconcern/$',RemoveConcern.as_view(),name='rfriend'),
    url(r'^addconcern/$',AddConcern.as_view(),name='afriend'),
)
