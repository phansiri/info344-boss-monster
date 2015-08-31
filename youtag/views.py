import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Video, Tag, TagVideo
from django.contrib.auth.models import User
from django.conf import settings



def video_list(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        tag_videos = TagVideo.objects.filter(owner=request.user)
        return render(request, 'youtag/video_list.html', {'tag_videos': tag_videos})

def tag_detail(request, pk):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        tags = TagVideo.objects.filter(tag=request.tag)
        return render(request, 'youtag/tag_detail.html', {'tags': tags})

