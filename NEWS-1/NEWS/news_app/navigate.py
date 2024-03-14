from news_app.models import Post, Tag, Category

def navigation(request):
    categories = Category.objects.all()[:5]
    tag = Tag.objects.all()[:10]
    trending_posts = Post.objects.filter(published_at__isnull=False, status="active").order_by("-views_count")[:3]
    return {
        "categories": categories,
        "tags": tag,
        "trending_posts":trending_posts,
    }