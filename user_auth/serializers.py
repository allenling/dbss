#coding=utf8
#coding:utf8
from django.contrib.auth import get_user_model

from avatar.models import Avatar
from avatar.util import get_default_avatar_url, get_primary_avatar

from rest_framework import serializers



class UserInCardOrNotField(serializers.RelatedField):
    
    def field_to_native(self, obj, field_name):
        if obj.follower.filter(id = self.context.get('pk')).exists():
            return self.to_native(True)
        else:
            return self.to_native(False)

    def to_native(self, value):
        return value

class FriendsAvatarField(serializers.RelatedField):

    def field_to_native(self, obj, field_name):
        try:
            a_path = get_primary_avatar(obj, 50)
            if a_path:
                return self.to_native(a_path.avatar_url(50, 50))
            else:
                return self.to_native(get_default_avatar_url())
        except Avatar.DoesNotExist:
            return self.to_native(get_default_avatar_url())

    def to_native(self, value):
        return value

class InviteFriends(serializers.ModelSerializer):

    avatar_set = FriendsAvatarField(many = True)

    class Meta:
       model = get_user_model()
       fields = ('id', 'username', 'avatar_set')

