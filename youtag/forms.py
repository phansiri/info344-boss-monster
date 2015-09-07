from django import forms

from .models import Video, Tag, TagVideo

# client side validation
# from parsley.decorators import parsleyfy

# @parsleyfy
class TagVideoForm(forms.Form):

    video = forms.URLField(label='Video URL', max_length=100)
    tag = forms.CharField(label='Tags', max_length=100)

    class Meta:
        model = TagVideo

