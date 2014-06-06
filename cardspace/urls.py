#coding=utf8
from django.conf.urls import patterns,  url
from django.contrib.auth.decorators import login_required

from dbss.cardspace.views import CardInfo, InviteFriends, CinviteFriendsList, CardInfoD, BlackList, WhiteList,\
        UserSnapList, UpdateFcard,FCardInfo, SearchFcardList, FuserGraphic, FuserGraphicy, FuserGraphicm, FuserGraphicd, EditFcard

urlpatterns = patterns('',
    url(r'^$',CardInfo.as_view(), name = 'cardinfo'),
    url(r'^user/(?P<userpk>\d+)/invitefriendlist/$',CinviteFriendsList.as_view(), name = 'cinvitefriendslist'),	
    url(r'^invitefriends/$',login_required(InviteFriends.as_view()), name = 'invitefriends'),	
    url(r'^cdriving/$',CardInfoD.as_view(), name = 'cardinfod'),	
    url(r'^blacklist/$',BlackList.as_view(), name = 'blist'),	
    url(r'^whitelist/$',WhiteList.as_view(), name = 'wlist'),	
    url(r'^users/$',UserSnapList.as_view(), name = 'cardusers'),	
    url(r'^update/(?P<fcard_pk>\d+)/$',login_required(UpdateFcard.as_view()), name = 'updatefcard'),	
    url(r'^fcards/(?P<user_pk>\d+)/$',FCardInfo.as_view(), name = 'fcard_info'),	
    url(r'^fcards/(?P<user_pk>\d+)/edit/$',EditFcard.as_view(), name = 'editfcard'),	
    url(r'^fcards/(?P<user_pk>\d+)/year/(?P<fyear>\d{4})/$',SearchFcardList.as_view(), name = 'sfl_year'),	
    url(r'^fcards/(?P<user_pk>\d+)/year/(?P<fyear>\d{4})/month/(?P<fmonth>\d{1,2})/$',SearchFcardList.as_view(), name = 'sfl_ymonth'),	
    url(r'^fcards/(?P<user_pk>\d+)/year/(?P<fyear>\d{4})/month/(?P<fmonth>\d{1,2})/day/(?P<fday>\d{1,2})/$',SearchFcardList.as_view(), name = 'sfl_ymday'),	
    url(r'^fcards/(?P<user_pk>\d+)/graphic/$',FuserGraphic.as_view(), name = 'graphic'),	
    url(r'^fcards/(?P<user_pk>\d+)/year/(?P<gyear>\d{4})/graphic/$',FuserGraphicy.as_view(), name = 'graphicyear'),	
    url(r'^fcards/(?P<user_pk>\d+)/year/(?P<gyear>\d{4})/month/(?P<gmonth>\d{1,2})/graphic/$',FuserGraphicm.as_view(), name = 'graphicmonth'),	
    url(r'^fcards/(?P<user_pk>\d+)/year/(?P<gyear>\d{4})/month/(?P<gmonth>\d{1,2})/day/(?P<gday>\d{1,2})/graphic/$',FuserGraphicd.as_view(), name = 'graphicday'),	
)
