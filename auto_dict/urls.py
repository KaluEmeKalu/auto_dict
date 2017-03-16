
from django.conf.urls import url


app_name = 'auto_dict'

from . import views
urlpatterns = [
    url(r'^$', views.index, name="index"),
]
