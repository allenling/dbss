#coding=utf-8
from django import template
register = template.Library()

@register.filter
def str_eq_int(value, arg):
    return str(value)==str(arg)

@register.filter
def trans_for_number(value):
    try:
        return int(value)
    except :
        return value
