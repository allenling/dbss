#coding=utf8
from django import forms

class SmessageForm(forms.Form):

    context = forms.Textarea()
    towho = forms.Textarea()
