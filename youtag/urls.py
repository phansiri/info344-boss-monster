from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.tag_list, name='tag_list'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.tag_detail, name='tag_detail'),
    url(r'^video/$', views.video_list, name='video_list'),
    url(r'^video/(?P<pk>[0-9]+)/$', views.video_detail, name='video_detail'),
    url(r'^video/(?P<pk>[0-9]+)/remove/$', views.video_remove, name='video_remove'),
    url(r'^video/new/$', views.video_new, name='video_new'),
    url(r'^api/$', views.ApiList),
    url(r'^api/(?P<pk>[0-9]+)/$', views.ApiDetail.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)