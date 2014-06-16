#coding=utf8
import simplejson
import math
import pickle


from django.core.mail import EmailMultiAlternatives

from redis_cache import get_redis_connection

from dbss.cardspace.models import Fcard, Graphic, PrivateCardPreuser

from dbss.user_auth.models import MyUser as User

class MyPaginate(object):
    '''
    paginate class
    '''
    phead = 1
    ptail = 1
    pageheadot = False
    pagetaildot = False
    def __init__(self, page, page_num):
        nowpage = page
        if nowpage - 1 > 4:
            self.phead = [nowpage - 4, nowpage - 3, nowpage - 2, nowpage - 1]
            self.pageheadot = True
        else:
            self.phead = range(1,nowpage)
            self.pageheadot = False
        if page_num - nowpage > 5:
            self.ptail = [nowpage + 1, nowpage + 2, nowpage + 3, nowpage + 4]
            self.pagetaildot = True
        else:
            self.ptail = range(nowpage+1,page_num+1)
            self.pagetaildot = False

    def generate_page(self, context_data):
        context_data['phead'] = self.phead
        context_data['pageheadot'] = self.pageheadot
        context_data['ptail'] = self.ptail
        context_data['pagetaildot'] = self.pagetaildot

class FcardUtils(object):
    '''
    fcard utils
    '''
    fcard = None
    now_date = None
    t_score = 0.1

    def __init__(self, fcard):
        self.fcard = fcard

    def add_graphic(self):
        graphic_r = get_redis_connection('graphic')
        fdate = self.fcard.pub_date
        self.nowdate = fdate
        graphic_rid = str(self.fcard.mcard.id)+'_'+str(self.fcard.carduser.id)
        try:
            grap = Graphic.objects.get(card = self.fcard.mcard, fcard = self.fcard.mfcard)
            grap_json = simplejson.loads(grap.graphic)
            t_year = grap_json.get(str(fdate.year))
            if t_year:
                t_month = t_year.get(str(fdate.month))
                if t_month:
                    t_day = t_month.get(str(fdate.day))
                    if t_day:
                        t_day.append(str(fdate.time())[:8])
                    else:
                        t_month[fdate.day] = [str(fdate.time())[:8]]
                else:
                    t_year.update({fdate.month:{fdate.day:[str(fdate.time())[:8]]}})
            else:
                date_json = dict({fdate.year:{fdate.month:{fdate.day:[str(fdate.time())[:8]]}}})
                grap_json.update(date_json)
            grap.graphic = simplejson.dumps(grap_json)
            grap.save(update_fields=['graphic'])
        except Graphic.DoesNotExist :
            grap_json = dict({fdate.year:{fdate.month:{fdate.day:[str(fdate.time())[:8]]}}})
            grap = Graphic(graphic = simplejson.dumps(grap_json), card = self.fcard.mcard, fcard = self.fcard.mfcard)
            grap.save()
            self.fcard.graphic = grap

        self.fcard.save(update_fields=['graphic'])

        #update graphic redis 
        try:
            nowdate_json = grap_json.get(str(fdate.year)).get(str(fdate.month))
        except AttributeError:
            nowdate_json = grap_json.get(fdate.year).get(fdate.month)

        self.update_gredis(graphic_r, graphic_rid, nowdate_json, fdate)


    def update_gredis(self, graphic_r, graphic_rid, nowdate_json, fdate):

        monc = graphic_r.hget(graphic_rid, str(fdate.year)+'_'+str(fdate.month)+'_s')
        if monc:
            monc = simplejson.loads(monc)
            if monc.get(str(fdate.day)):
                z=int(monc.get(str(fdate.day)))+1
                monc[str(fdate.day)] = z
            else:
                tmpday = {fdate.day:1}
                monc.update(tmpday)
        else:
            monc = {fdate.day:1}
        graphic_r.hset(graphic_rid, str(fdate.year)+'_'+str(fdate.month)+'_s', simplejson.dumps(monc))

        year_cc = graphic_r.hget(graphic_rid, str(fdate.year)+'_c')
        graphic_r.hset(graphic_rid, str(fdate.year)+'_c', int(year_cc)+1 if year_cc else 1)

        month_cc = graphic_r.hget(graphic_rid, str(fdate.year)+'_'+str(fdate.month)+'_c')
        graphic_r.hset(graphic_rid, str(fdate.year)+'_'+str(fdate.month)+'_c', int(month_cc)+1 if month_cc else 1)
        graphic_r.hset(graphic_rid, str(fdate.year)+'_'+str(fdate.month)+'_d',simplejson.dumps(nowdate_json))
        
        yyear = graphic_r.hget(graphic_rid, str(fdate.year))
        if yyear:
            yyear = simplejson.loads(yyear)
            nowm = yyear.get(str(fdate.month))
            if nowm == None:
                yyear.update({fdate.month:[fdate.day]})
            elif fdate.day not in nowm:
                nowm.append(fdate.day)
        else:
            yyear = {fdate.month:[fdate.day]}
        graphic_r.hset(graphic_rid, str(fdate.year), simplejson.dumps(yyear))



    def get_score(self, daydiff, prevdaydiff):
        if daydiff is 0:
            df = prevdaydiff + 1
        elif daydiff is 1:
            df = prevdaydiff
        else:
            df = prevdaydiff + daydiff -1
        df = prevdaydiff + daydiff
        return (round(0.1/math.pow(df-1,1.1),5),df - 1 if daydiff <= prevdaydiff else df )

    def set_score(self):
        if self.fcard.prevcard.id != self.fcard.id:
            prevdate = self.fcard.prevcard.pub_date
            nowdate = self.fcard.pub_date
            daydiff = nowdate - prevdate
            prevdaydiff = self.fcard.prevcard.daydiff
            prev_score = self.fcard.prevcard.score

            (self.t_score, t_daydiff) = self.get_score(daydiff.days, prevdaydiff)
            self.fcard.score = prev_score + self.t_score
            self.fcard.daydiff = int(t_daydiff)
            self.fcard.save(update_fields = ['score', 'daydiff'])

    def cal_card_score(self):
        self.fcard.mcard.score = self.fcard.mcard.score + round(0.1*self.t_score,5)
        self.fcard.mcard.save(update_fields=['score'])


def distr_object(t_object, **kwargs):
    redis_c = get_redis_connection('feed_storage')
    rfeed_list = kwargs.get('feed_list') 
    rt_object = pickle.dumps(t_object)
    if t_object.get_verbtext() == 'updatefcard':
        redis_fa = get_redis_connection('favlist')
        for i in rfeed_list:
            action = redis_fa.hget(str(i), t_object.get_mobject_id())
            if action.startswith('A') or (action.startswith('B') and str(i) in action):
                redis_c.lpush(str(i), rt_object)
    else:
        for i in rfeed_list:
            redis_c.lpush(i, rt_object)

def remail_user(inuser, subject, message):
    e = EmailMultiAlternatives(subject, message, 'dbss@gmail.com', [inuser.email])
    htmlcon = ''''<p >welcome!</p>'''
    e.attach_alternative(htmlcon, 'text/html')
    e.send()

def updatefcard(fcard_id):
    fu = FcardUtils(Fcard.objects.get(pk = fcard_id))
    fu.add_graphic()
    fu.set_score()
    fu.cal_card_score()

def newfavlist(user_id, card_id):
    favlist_r = get_redis_connection('favlist')
    favlist_r.hset(str(user_id), card_id, 'A')

def deletefavlist(user_id, card_id):
    favlist_r = get_redis_connection('favlist')
    favlist_r.hdel(str(user_id), card_id)

def updatefavlist(user_id, card_id, action, target):
    favlist_r = get_redis_connection('favlist')
    fa_list = favlist_r.hget(str(user_id), card_id)
    if fa_list == None or fa_list[0] != action :
        if target != None:
            action = action +'_'+target
        favlist_r.hset(str(user_id), card_id, action)
    else:
        new_action = fa_list + '_'+target
        favlist_r.hset(str(user_id), card_id, new_action)

def update_msg(redis_connnect, rindex, status, content):
    isnone = redis_connnect.lpop(rindex)
    content['status'] = status
    if isnone != None:
        isnone = simplejson.loads(isnone)
        del isnone['status']
        redis_connnect.lpush(rindex, simplejson.dumps(isnone))
    if redis_connnect.llen(rindex) > 500:
        redis_connnect.rpop(rindex)
    redis_connnect.lpush(rindex, simplejson.dumps(content))

def store_msg(redis_connnect, content):
    whostr = str(content['who_id'])+'_'+ str(content['towho_id'])
    tostr = str(content['towho_id'])+'_'+str(content['who_id'])
    redis_connnect.zincrby(content['who_id'], content['towho_id'])
    redis_connnect.zincrby(content['towho_id'], content['who_id'])
    update_msg(redis_connnect, whostr, 'read', content)
    update_msg(redis_connnect, tostr, 'unread', content)
    #increment unread msg count
    redis_connnect.incr('unread_'+content['towho_id'])

def send_message(content, ulist, action, property, objid = None):
    userobjlist = []
    msg_redis = get_redis_connection('message')
    for i in ulist:
        try:
            tmpi = User.objects.get(username = i)
        except User.DoesNotExist:
            continue
        if content['who_id'] == tmpi:
            continue
        userobjlist.append(tmpi.id)
        content['towho_id'] = tmpi.id
        content['towho_username'] = i
        store_msg(msg_redis, content)
    if property == 'Private' and action == 'Invite':
        preuserlist = PrivateCardPreuser.objects.get_or_create(privatecard__id = objid)
        for i in userobjlist:
            preuserlist[0].preuser.add(i)

def get_unread_msg(request):
    
    msg_redis = get_redis_connection('message')
    if request.user.is_anonymous() == False and request.user.is_authenticated():
        umsg = msg_redis.get('unread_' + str(request.user.id))
        return True if umsg is not None and int(umsg) > 0 else False
