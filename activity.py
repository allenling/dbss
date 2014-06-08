#coding=utf8
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse


VERB_DICT = {
    'createpubcard': ''' 创建了一个公开的活动卡''',
    'createpricard': ''' 创建了一个私密的活动卡''',
    'invitepub': ''' 邀请你加入一个公开的活动''',
    'invitepri': ''' 邀请你加入一个私密的活动''',
    'updatefcard': ''' 更新了一个活动''',
}

class Activity(object):

    def __init__(self, object_id, muser, user_name, c_date, thumbcontent, mobject_id, mtitle, verb):
        self.object_id = object_id
        self.muser = muser
        self.user_name = user_name
        self.date = c_date
        self.thumbcontent = thumbcontent
        self.mobject_id = mobject_id
        self.mtitle = '''<a href="'''+reverse('cardspace:cardinfo', kwargs={'pk':self.mobject_id})+'''">'''+mtitle+'''</a>'''
        self.verb = '''<a href="'''+reverse('cardspace:cardinfo',kwargs={'pk':self.muser})+'''">'''+self.user_name+'''</a>'''+VERB_DICT.get(verb)
        self.verbtext = verb

    def __unicode__(self):
        return self.verbtext+'-->'+self.user_name

    def get_object_id(self):
        return self.object_id

    def get_muser(self):
        return self.muser

    def get_user_name(self):
        return self.user_name

    def get_date(self):
        return self.c_date

    def get_thumbcontent(self):
        return self.thumbcontent

    def get_mobject_id(self):
        return self.mobject_id
    
    def get_mtitle(self):
        return self.mtitle

    def set_real_user(self):
        self.ruser = get_user_model().objects.get(pk=self.muser)

    def get_verbtext(self):
        return self.verbtext

    def get_verb(self):
        return self.verb
