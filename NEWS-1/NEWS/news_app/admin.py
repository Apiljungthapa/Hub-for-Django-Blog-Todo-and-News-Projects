from django.contrib import admin
from news_app.models import Post, Tag, Category, Contact, UserProfile, Comment, NewsLetter

from django_summernote.admin import SummernoteModelAdmin
from .models import Post

# Register your models here.
# admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(NewsLetter)




class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Post, PostAdmin)