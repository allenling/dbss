#coding=utf8
import re
from bs4 import BeautifulSoup

from django.db import models
from django.db.models import signals
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.encoding import smart_unicode, smart_text
from django.utils import timezone

from ckeditor.fields import RichTextField
import django_rq
from redis_cache import get_redis_connection
from haystack.management.commands import update_index

from dbss.user_auth.models import MyUser as User
from dbss.activity import Activity

class BaseCard(models.Model):
    
    context = RichTextField()
    pub_date = models.DateTimeField(auto_now_add = True)
    score = models.FloatField(default = 1)

    class Meta:
        abstract = True

    def get_context_thumb_txt(self, context_bea):
        tmp_txt = context_bea.get_text()
        one_blank = re.compile('\s+')
        tmp_txt = smart_unicode(one_blank.sub(' ',tmp_txt.strip()))[:100]
        return tmp_txt

    def get_context_thumb(self):
        context_b = BeautifulSoup(self.context)
        real_text = self.get_context_thumb_txt(context_b)
        img_result = context_b.find('img')
        if img_result:
            return ('img', str(img_result), real_text)
        embed_result = context_b.find('embed')
        if embed_result:
            return ('embed', str(embed_result['src']), real_text)
        return ('text', None, real_text)

    def create_activity(self, verb):
        user_name = self.carduser.get_full_name
        c_date = self.getpubdate()
        thumbcontent = self.get_context_thumb()
        mobject_id = self.get_mobject()
        mtitle = self.get_mtitle()
        ac = Activity(object_id = self.id, muser = self.carduser.id, user_name = user_name, c_date = c_date, thumbcontent = thumbcontent, mobject_id = mobject_id, mtitle = mtitle, verb = verb)
        return ac

    def getpubdate(self):
        return timezone.localtime(self.pub_date).__str__()[:19]

class Fcard(BaseCard):

    carduser = models.ForeignKey(User, related_name = 'fcarduser')
    mcard = models.ForeignKey('Card', related_name = 'maincard')
    mfcard = models.ForeignKey('self', related_name = 'mainfcard', null = True, blank = True)
    prevcard = models.ForeignKey('self', related_name = 'prev', null = True, blank = True)
    nextcard = models.ForeignKey('self', related_name = 'next', null = True, blank = True)
    graphic = models.ForeignKey('Graphic', related_name = 'f_graphic', null = True, blank = True)
    daydiff = models.IntegerField(default = 1)

    class Meta:
        ordering = ['-pub_date',]

    def __unicode__(self):
        return self.carduser.username+'_'+self.mcard.title+'_'+str(self.pub_date)[:16]

    def get_mobject(self):
        return self.mcard.id

    def get_mtitle(self):
        return self.mcard.title

class Card(BaseCard):
    '''
    Card Model
    '''
    title = models.CharField(max_length = 20)
    carduser = models.ForeignKey(User, related_name = 'initator')
    users = models.ManyToManyField(User, blank = True, null = True, related_name = 'follower')
    tags = models.ManyToManyField('CardTag', related_name = 'ctag') 
    isclose = models.BooleanField(default = False)
    PROPERTY=(
        ('Public','Public'),
        ('Private','Private'),
    )
    property = models.CharField(max_length = 7, choices = PROPERTY, default = 'Public')

    class Meta:
        '''
        Card Model Meta
        '''
        ordering = ['-score','-pub_date']
        permissions = (('private_access', 'private card access limit'),)

    def __unicode__(self):
        return self.carduser.username+' '+self.title

    def close(self):
        self.isclose = True

    def getrecent(self):
        try:
            return self.maincard.latest('pub_date')
        except Fcard.DoesNotExist:
            return None

    def getitle(self):
        return smart_text(self.title)[:30]

    def getusercount(self):
        count =""
        ucount = self.users.count()
        if ucount > 99:
            count = str(ucount)
            return count
        elif ucount > 0:
            count = str(ucount)
            return count
        elif ucount == 0:
            return count
    
    def getagstxt(self):
        tags = self.tags.all()
        return [smart_unicode(i.tag)[:10] for i in tags]

    def get_first_ten_users(self):
        return  self.users.order_by('-date_join')[:10]

    def get_absolute_url(self):
        return reverse('cardspace:cardinfo', kwargs={'pk':self.id})

    def get_mobject(self):
        return self.id

    def get_mtitle(self):
        return self.title


class Graphic(models.Model):
    graphic = models.TextField()
    fcard = models.ForeignKey(Fcard, related_name = 'fcard_grap')
    card = models.ForeignKey(Card, related_name = 'card_grap')

    def __unicode__(self):
        return self.card.__unicode__()+'_'+self.fcard.carduser.get_full_name

class CardTag(models.Model):
    '''
    CardTag class
    '''
    tag = models.CharField(max_length = 15, unique = True)
    allc = models.BigIntegerField(default = 0)
    pub_date = models.DateTimeField(auto_now_add = True)


    def __unicode__(self):
        return self.tag

    def getname(self):
        return smart_unicode(self.tag)[:12]

    def get_absolute_url(self):
        return reverse('tagspage')


class PrivateCardPreuser(models.Model):
    privatecard = models.OneToOneField(Card, related_name = 'private_card')
    preuser = models.ManyToManyField(User, related_name = 'prev_user')

    def __unicode__(self):
        return self.privatecard.title+'_prevuser'

def cron_update_index(sender, **kwargs):
    index_redis = get_redis_connection('djrq')
    index_count = int(index_redis.incr(settings.INDEX_NAME))
    if index_count > settings.INDEX_COUNT + 1:
        index_redis.set(settings.INDEX_NAME, 0)
        index_queue = django_rq.get_queue(settings.INDEX_QUEUE)
        if index_queue.count < 1:
            index_queue.enqueue(warp_update_index)

def warp_update_index():
    update_index.Command().handle()

signals.post_save.connect(cron_update_index, sender=Card, dispatch_uid='unique_save') 
