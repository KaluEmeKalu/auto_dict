
from django.conf.urls import url


app_name = 'auto_dict'

from . import views
urlpatterns = [
    url(r'^tables', views.tables, name='tables'),
    url(r'^word_search/make_anki', views.make_anki_text, name='make_anki_text'),
    url(r'^word_search/', views.word_search, name='word_search'),
    url(r'^$', views.index, name="index"),
]
