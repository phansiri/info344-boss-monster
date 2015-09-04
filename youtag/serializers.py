from django.forms import widgets
from rest_framework import serializers
from .models import Tag, Video, TagVideo
from django.contrib.auth.models import User

class TagVideoSerializer(serializers.ModelSerializer):

    video = serializers.PrimaryKeyRelatedField(many=False, queryset=Video.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = TagVideo
        fields = ('owner',
                  'created',
                  'video',
                  'tags',)