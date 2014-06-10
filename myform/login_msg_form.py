#coding=utf8
from django.contrib.auth.forms import AuthenticationForm


class LoginMsgForm(AuthenticationForm):

    error_messages = {
        'invalid_login': '输入的用户名或者密码不正确',
        'no_cookies': '您的浏览器没有开启cookie功能, 登陆需要您开启cookie功能',
        'inactive': '该账号已被冻结，请与管理员联系',
    }
