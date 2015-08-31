from django.db import models
from django.utils import timezone


class Video(models.Model):
    vidId = models.CharField(max_length=30)
    title = models.CharField(max_length=400)
    desc = models.CharField(max_length=400)

    def __str__(self):
        return self.vidId

class Tag(models.Model):
    word = models.TextField()

    def __str__(self):
        return self.word

class TagVideo(models.Model):
    owner = models.ForeignKey('auth.User')
    video = models.ForeignKey(Video)
    tag = models.ForeignKey(Tag)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id
