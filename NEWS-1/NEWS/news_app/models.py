from django.db import models

# Create your models here.

class base_model(models.Model):
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True # django le table banudaina


class Category(base_model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
   

class Tag(base_model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    


class Post(base_model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('in_active', 'Inactive'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="post_images/%y/%m/%d", blank=False)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='news_posts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    views_count = models.PositiveBigIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    tag = models.ManyToManyField(Tag)

    
    def __str__(self):
        return self.title

class Contact(base_model):
    message = models.TextField()
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class UserProfile(base_model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="user_images/%Y/%m/%d", blank=False)
    address = models.CharField(max_length=200)
    biography = models.TextField()
    
    def __str__(self):
        return self.user.username

class Comment(base_model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    name = models.CharField(max_length=50)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.email} | {self.comment[:70]}"\


class NewsLetter(base_model):
    email = models.EmailField()

    def __str__(self):
        return f"{self.email}"
    
   


    
        

    

    