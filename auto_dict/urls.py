
from django.conf.urls import url
from . import views


app_name = 'auto_dict'

urlpatterns = [
    url(r'^tables', views.tables, name='tables'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.UserLoginView.as_view(), name="login"),
    url(r'^word_search/make_anki', views.make_anki_text, name='make_anki_text'),
    url(r'^word_search/', views.word_search, name='word_search'),
    url(r'^textfile_word_search/', views.textfile_word_search, name='textfile_word_search'),
    url(r'^$', views.school_class_dashboard, name="index"),
    url(r'^exam/(?P<exam_id>[0-9]+)/(?P<turn_in>[-\w]+)/$', views.exam, name="exam"),
    url(r'^exam/(?P<exam_id>[0-9]+)/', views.exam, name="exam"),
    url(r'^class/(?P<school_class_id>[0-9]+)/', views.school_class_dashboard, name="school_class_dashboard"),
    url(r'^turn_in_exam/(?P<exam_paper_id>[0-9]+)/$', views.turn_in_exam, name="turn_in_exam"),
    # url(r'^exam/(?P<exam_id>[0-9]+)/save_answer/$', views.save_answer, name="save_answer"),
    url(r'^save_answer/$', views.save_answer, name="save_answer"),
    url(r'^logout/$', views.user_logout, name="logout"),
    url(r'^change_user_image/$', views.change_user_image, name='change_user_image'),
    url(r'create_post/(?P<school_class_id>[0-9]+)/$', views.PostCreate.as_view(), name='create_post'),
    # url(r'^video/(?P<pk>[0-9]+)/$',
    #     views.VideoDetailView.as_view(), name="video"),
    url(r'^video/(?P<video_id>[0-9]+)/$',
        views.video_view, name="video"),
    url(r'^mark_video_watched/(?P<video_id>[0-9]+)/$',
        views.mark_video_watched, name="mark_video_watched")
]
