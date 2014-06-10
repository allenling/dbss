#coding=utf8
import simplejson

from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils.encoding import smart_text

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self,username,email,password,something = None):
        user = self.model(username=username, email = MyUserManager.normalize_email(email),something = something, is_active=False,is_staff=False,is_superuser=False)
        if not username and not email:
            raise ValueError('username and email must be set')
        user.set_password(password)
        user.favlist = simplejson.dumps({})
        user.save(using=self._db)
        return user
    def create_superuser(self, email,username,password,something='Nothing'):
        user = self.create_user(email = email,username = username,password=password,something=something)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using = self._db)
        return user
    '''
    def create_superuser(self,email,username,password, something='Nothing'):
    user = self.create_user(email=email,username=username,password=password,something=something)
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save(using = self._db)
    return user
'''

class MyUser(AbstractBaseUser, PermissionsMixin):
    username=models.CharField(max_length=12,unique=True,db_index=True)
    email=models.EmailField(max_length=100,unique=True)
    date_join=models.DateTimeField(auto_now_add=True)
    last_join=models.DateTimeField(auto_now=True)
    something=models.CharField(max_length=13,blank=True,null=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    objects=MyUserManager()
    favlist=models.TextField(blank = True, null=True,)
    friends = models.ManyToManyField('self', null = True, blank = True, related_name = 'friends')
    score = models.IntegerField(default = 1)
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['email',]
    
    @property
    def get_full_name(self):
        return smart_text(self.username)
    def get_short_name(self):
        return smart_text(self.username)
    def __unicode__(self):
        return smart_text(self.username)

    def get_something(self):
        return smart_text(self.something)

    def isrequestfriend(self, requestu):
        if requestu.is_anonymous() == False and requestu.is_authenticated():
            self.isrefriend = self.friends.filter(pk=requestu.id).exists()
        else:
            self.isrefriend = False

    def requestconcernme(self, requestu):
        if requestu.is_anonymous() == False and requestu.is_authenticated():
            self.rconcernme = UserFollow.objects.filter(fuser__pk=requestu.id, tuser__pk = self.id).exists()
        else:
            self.rconcernme = False

    def meconcernrequest(self, requestu):
        if requestu.is_anonymous() == False and requestu.is_authenticated():
            self.meconcernr = UserFollow.objects.filter(fuser__pk=self.id, tuser__pk = requestu.id).exists()
        else:
            self.meconcernr = False

    def concernrequest(self, requestu):
         tmp = UserFollow.objects.get_or_create(fuser_id = self.id, tuser_id = requestu.id)[0]
         tmp.save()

    def requestconcern(self, requestu):
         tmp = UserFollow.objects.get_or_create(fuser_id = requestu.id, tuser_id = self.id)[0]
         tmp.save()

    def removeconcernr(self, requestu):
         tmp = UserFollow.objects.get(fuser_id = self.id, tuser_id = requestu.id)
         tmp.delete()

    def removerconcern(self, requestu):
         try:
            tmp = UserFollow.objects.get(fuser_id = requestu.id, tuser_id = self.id)
         except UserFollow.DoesNotExist:
            pass
         else:
            tmp.delete()

    def addfriends(self, requestu):
        self.friends.add(requestu)

    def removefriends(self, requestu):
        self.friends.remove(requestu)

    def has_unread(self):
        pass


class UserFollow(models.Model):

    fuser = models.ForeignKey(MyUser, related_name = 'fuser')
    tuser = models.ForeignKey(MyUser, related_name = 'tuser')

    def __unicode__(self):
        return self.fuser.get_full_name+'_follow_'+self.tuser.get_full_name
