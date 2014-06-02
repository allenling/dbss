#coding=utf8
from django.forms import ModelForm
from django import forms

from dbss.cardspace.models import  Message

class SmessageForm(ModelForm):

    context = forms.Textarea()
    towho = forms.Textarea()

    class Meta:

        model = Message
        fields = ('towho', 'context',)
