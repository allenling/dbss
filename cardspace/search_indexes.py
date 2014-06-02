#coding=utf8
from datetime import datetime
from haystack import indexes
from dbss.cardspace.models import Card, CardTag

class CardIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr = 'title')
    property = indexes.CharField(model_attr = 'property')
    pub_date = indexes.DateTimeField(model_attr = 'pub_date')

    def get_model(self):
        return Card

    def index_queryset(self, using = None):
        return self.get_model().objects.filter(pub_date__lte = datetime.now())

class TagIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document = True, use_template = True)
    tag = indexes.CharField(model_attr = 'tag')

    def get_model(self):
        return CardTag

    def index_queryset(self, using = None):
        return self.get_model().objects.filter(pub_date__lte = datetime.now())
