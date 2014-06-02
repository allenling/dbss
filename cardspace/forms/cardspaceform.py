#coding=utf8
from django.forms import ModelForm
from django import forms

from haystack.forms import ModelSearchForm

from ckeditor.widgets import CKEditorWidget
from dbss.cardspace.models import Card,Fcard


class CardNewForm(ModelForm):

	title=forms.CharField(max_length=60,)
	context = forms.CharField(widget = CKEditorWidget())
	PROPERTY=(
		('Public','Public'),
		('Private','Private'),
	)
	property=forms.ChoiceField(choices=PROPERTY)


	class Meta:
		model=Card
		fields=('title', 'context','property')


class FCardNewForm(ModelForm):

	context = forms.CharField(widget = CKEditorWidget())


	class Meta:
		model=Fcard
		fields=('context',)

class CardSpaceSearchForm(ModelSearchForm):
    
    def search(self):
        self.searchqueryset = Card.objects.filter(property = 'Public')
        return super(CardSpaceSearchForm, self).search()
