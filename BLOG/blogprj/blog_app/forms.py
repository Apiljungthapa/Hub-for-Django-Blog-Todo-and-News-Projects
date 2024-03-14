from django import forms
from blog_app.models import post

class Postform(forms.ModelForm):
    class Meta:
        model = post
        fields=["title","content"]