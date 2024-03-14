from django.db import models

# Create your models here.
class post(models.Model):
    title = models.CharField(max_length=280)
    content = models.TextField()
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
