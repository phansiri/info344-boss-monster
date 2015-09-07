import requests, time, json
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

from youtag.models import Video, Tag, TagVideo
from youtag.forms import TagVideoForm
from youtag.serializers import TagVideoSerializer
from youtag.permissions import IsOwnerOrReadOnly
from mysite.settings import DEVELOPER_KEY

from ratelimit.decorators import ratelimit
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from ratelimit.mixins import RatelimitMixin


# This view gives a list of all the videos a user has uploaded
@login_required(login_url='accounts/login/')
def video_list(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        tag_videos = TagVideo.objects.filter(owner=request.user)
        return render(request, 'youtag/video_list.html', {'tag_videos': tag_videos})


# This view gives a oomplete list of all the tags a person has in their videos
@login_required(login_url='accounts/login/')
def tag_list(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        tags = Tag.objects.filter(tagvideo__owner=request.user).distinct()
        return render(request, 'youtag/tag_list.html', {'tags': tags})


# This view gives a detail view of a tag, along with the videos associated with it
@login_required(login_url='accounts/login/')
def tag_detail(request, pk):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        try:
            tag = get_object_or_404(Tag, pk=pk)
            videos = Video.objects.filter(tagvideo__tags__id=tag.id, tagvideo__owner=request.user)
        except:
            return render(request, 'youtag/tag_detail.html', {'errors': ('That tag does not exist.',)})
        return render(request, 'youtag/tag_detail.html', {'tag': tag, 'videos': videos})


# This view gives a complete detail of a particular tagged video
@login_required(login_url='accounts/login/')
def video_detail(request, pk):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        tagvideo = get_object_or_404(TagVideo, pk=pk)
        video = get_object_or_404(Video, pk=tagvideo.video.id)

        # generate the list of tags
        taglist = tagvideo.tags.all()
        tags = []
        for tag in taglist:
            tags.append(tag.word)

        return render(request, 'youtag/video_detail.html', {'video': video,
                                                            'tagvideo': tagvideo,
                                                            'tags': tags})

# This view allows you to delete a video
@login_required(login_url='accounts/login/')
def video_remove(request, pk):
    tagvideo = get_object_or_404(TagVideo, pk=pk)
    tagvideo.delete()
    redirect_url = '../../../'
    return redirect(redirect_url)

# This view will create a new listing for the user which contains the video they wish
# to list along with all the tags associated with it
@login_required(login_url='accounts/login/')
def video_new(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == 'POST':
            form = TagVideoForm(request.POST)
            if form.is_valid():

                # deconstruct the url
                try:
                    split_url = request.POST['video'].split('?')
                    split_url = split_url[1].split('&')

                    for split in split_url:
                        if split.find('v=') >= 0:
                            bits = split.split('=')
                            vidId = bits[1]
                except:
                    return render(request, 'youtag/tagvideo_new.html', {'form': form, 'errors': ('The URL was not properly formatted.',)})

                # check and see if the video id exists already
                try:
                    video = Video.objects.get(vidId=vidId)
                    # if they have this video already, send them away
                    tagvideo = TagVideo.objects.get(video=video, owner=request.user)
                    if tagvideo is not None:
                        return render(request, 'youtag/tagvideo_new.html', {'form': form, 'errors': ('That video already has been tagged.',)})
                except:
                    # if not, build a new video
                    video = Video()
                    video.vidId = vidId
                    video.title = ''
                    video.desc = ''

                    # grab the video from the YouTube servers
                    try:
                        querystring = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&key=' + DEVELOPER_KEY + '&id=' + vidId
                        results = json.loads(requests.request('GET', querystring).text)
                        video.title = results['items'][0]['snippet']['title']
                        video.desc = results['items'][0]['snippet']['description']

                    except:
                        return render(request, 'youtag/tagvideo_new.html', {'form': form, 'errors': ('That video was not found.',)})

                # start assigning data
                video.save()
                tagvideo = TagVideo()
                tagvideo.video = video
                tagvideo.owner = request.user
                tagvideo.created = timezone.now()
                tagvideo.save()

                # split up the tags
                taglist = request.POST['tag'].replace(' ', '')
                taglist = taglist.split(',')

                for tag in taglist:
                    try:
                        tag_obj = Tag.objects.get(word=tag)
                    except:
                        tag_obj = Tag.objects.create(word=tag)
                    # add in the tag association
                    if not tag == '':
                        tag_obj.save()
                        tagvideo.tags.add(tag_obj)

                # save them all!
                tagvideo.save()

                # CREATED!
                redirect_url = '../' + str(tagvideo.id)
                return redirect(redirect_url)
            else:
                return render(request, 'youtag/tagvideo_new.html', {'form': form, 'errors': ('There was errors in your submission.',)})

        else:
            form = TagVideoForm()
            return render(request, 'youtag/tagvideo_new.html', {'form': form})



# # API VIEWS
# It gets all weird in here!

# API Detail allows you to retrieve a TagVideo
# Update and Delete is only allowed if you are the owner
class ApiDetail(RatelimitMixin, generics.RetrieveUpdateDestroyAPIView):
    ratelimit_key = 'ip'
    ratelimit_rate = '10/m'
    ratelimit_block = True
    ratelimit_method = 'GET', 'PUT', 'DELETE'

    queryset = TagVideo.objects.all()
    serializer_class = TagVideoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


# API List allows you to see the list of all your TagVideos
# Create is allowed if you are authenticated

@login_required(login_url='../api-auth/login/')
@api_view(['GET','POST'])
def ApiList(request, format=None):
    if request.method == 'GET':
        tagvideos = TagVideo.objects.filter(owner=request.user)
        serializer = TagVideoSerializer(tagvideos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated():
            return Response('You are not logged in.', status=status.HTTP_400_BAD_REQUEST)
        else:
            data = json.loads(request.POST['_content'])

            # deconstruct the url
            try:
                split_url = data['url'].split('?')
                split_url = split_url[1].split('&')

                for split in split_url:
                    if split.find('v=') >= 0:
                        bits = split.split('=')
                        vidId = bits[1]
            except:
                return Response('url is not valid.', status=status.HTTP_400_BAD_REQUEST)

            # make sure a list of tags is included
            try:
                taglist = data['tags'].replace(' ', '')
            except:
                return Response('Please include a comma-separated list of tags.', status=status.HTTP_400_BAD_REQUEST)


            try:
                video = Video.objects.get(vidId=vidId)
                # if they have this video already, send them away
                tagvideo = TagVideo.objects.get(video=video, owner=request.user)
                if tagvideo is not None:
                    return Response('This video has already been tagged.', status=status.HTTP_400_BAD_REQUEST)
            except:
                # if not, build a new video
                video = Video()
                video.vidId = vidId
                video.title = ''
                video.desc = ''

            # grab the video from the YouTube servers
            try:
                querystring = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&key=' + DEVELOPER_KEY + '&id=' + vidId
                results = json.loads(requests.request('GET', querystring).text)
                video.title = results['items'][0]['snippet']['title']
                video.desc = results['items'][0]['snippet']['description']

            except:
                return Response('That Youtube video does not exist.', status=status.HTTP_400_BAD_REQUEST)

            # start assigning data
            video.save()
            tagvideo = TagVideo()
            tagvideo.video = video
            tagvideo.owner = request.user
            tagvideo.created = timezone.now()
            tagvideo.save()

            # split up the tags
            taglist = taglist.split(',')

            for tag in taglist:
                try:
                    tag_obj = Tag.objects.get(word=tag)
                except:
                    tag_obj = Tag.objects.create(word=tag)
                # add in the tag association
                if not tag == '':
                    tag_obj.save()
                    tagvideo.tags.add(tag_obj)

            # save them all!
            tagvideo.save()

            return Response(status=status.HTTP_201_CREATED)
    else:
        return Response('This node only accepts GET and POST', status=status.HTTP_400_BAD_REQUEST)



