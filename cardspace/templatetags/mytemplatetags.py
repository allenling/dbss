#coding=utf-8
from django import template
register = template.Library()

@register.filter
def str_eq_int(value, arg):
    return str(value)==str(arg)