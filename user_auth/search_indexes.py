#coding=utf8
from datetime import datetime
from haystack import indexes
from dbss.user_auth.models import MyUser

class MyuserIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    username = indexes.CharField(model_attr = 'username')
    something = indexes.CharField(model_attr = 'something')
    date_join = indexes.DateTimeField(model_attr = 'date_join')

    def get_model(self):
        return MyUser

    def index_queryset(self, using = None):
        return self.get_model().objects.filter(date_join__lte = datetime.now())
