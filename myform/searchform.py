#coding=utf-8

from haystack.forms import ModelSearchForm

from haystack.query import SearchQuerySet

from dbss.cardspace.models import Card, CardTag
from dbss.user_auth.models import MyUser

class SearchForm(ModelSearchForm):
    
    def search(self):
        sql = SearchQuerySet()
        models_str = self.get_models()[0]

        if models_str == Card:
            return sql.filter(title = self.cleaned_data['q'])
        elif models_str == CardTag:
            return sql.filter(tag = self.cleaned_data['q'])
        elif models_str == MyUser:
            return sql.filter(username = self.cleaned_data['q'])
