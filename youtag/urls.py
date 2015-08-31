from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.video_list, name='video_list'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.tag_detail, name='tag_detail'),
]