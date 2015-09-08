from django.db import models
from django.utils import timezone

# # Video object
class Video(models.Model):
    vidId = models.CharField(max_length=30)
    title = models.CharField(max_length=400)
    desc = models.CharField(max_length=400)

    def __str__(self):
        return self.vidId


# # Tag object
class Tag(models.Model):
    word = models.TextField()

    def __str__(self):
        return self.word

# # TagVideo object
class TagVideo(models.Model):
    owner = models.ForeignKey('auth.User')
    video = models.ForeignKey(Video)
    tags = models.ManyToManyField(Tag)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)
