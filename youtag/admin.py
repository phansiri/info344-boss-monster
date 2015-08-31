from django.contrib import admin
from .models import Video, Tag, TagVideo

admin.site.register(Video)
admin.site.register(Tag)
admin.site.register(TagVideo)
