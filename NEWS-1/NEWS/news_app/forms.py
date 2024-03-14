from django import forms
from news_app.models import Contact,Comment,NewsLetter

class contactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields="__all__" #django le sabai model ma vako jati field haru rakhdinxa afai
       #fields=['message','name','email','subject']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields="__all__" #django le sabai model ma vako jati field haru rakhdinxa afai
       #fields=['message','name','email','subject']
        

class NewsLetterForm(forms.ModelForm):

    class Meta:
        model = NewsLetter
        fields="__all__"