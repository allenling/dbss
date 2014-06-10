#coding=utf8
from dbss.utils import get_unread_msg

def unreadmsg(request):
    '''
    查看用户是否存在未读的信息
    '''
    return {'hasunread': get_unread_msg(request)}
