#coding=utf8
from dbss.cardspace.models import Card, Fcard, CardTag, Graphic, PrivateCardPreuser
from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextField

class CardAdminForm(forms.ModelForm):
    context = forms.CharField(widget = CKEditorWidget())
    class Meta:
        model = Card

class CardAdmin(admin.ModelAdmin):
    '''
    card admin
    '''
    context = RichTextField()
    #form = CardAdminForm
    readonly_fields=('pub_date', )
    search_fields = ('property', 'pub_date')
    ordering = ('-pub_date',)


class FCardAdmin(admin.ModelAdmin):
    '''
    follow card admin
    '''
    readonly_fields=('pub_date', )	


class MessageAdmin(admin.ModelAdmin):
    '''
    message admin
    '''
    readonly_fields=('pub_date', )	


class CardTagAdmin(admin.ModelAdmin):
    '''
    card tag admin
    '''
    readonly_fields = ('pub_date',)



admin.site.register(Card, CardAdmin)
admin.site.register(Fcard, FCardAdmin)
admin.site.register(CardTag, CardTagAdmin)
admin.site.register(Graphic)
admin.site.register(PrivateCardPreuser)
