
from django.conf.urls import url


app_name = 'auto_dict'

from . import views
urlpatterns = [
    url(r'^tables', views.tables, name='tables'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.UserLoginView.as_view(), name="login"),
    url(r'^word_search/make_anki', views.make_anki_text, name='make_anki_text'),
    url(r'^word_search/', views.word_search, name='word_search'),
    url(r'^$', views.index, name="index"),
    url(r'^logout/$', views.user_logout, name="logout"),
    url(r'^change_user_image/$', views.change_user_image, name='change_user_image'),
]
