from django.shortcuts import render,redirect
from blog_app.models import post
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import Postform




# Create your views here.

def post_list(request):
    posts = post.objects.filter(published_at__isnull=False).order_by("-published_at")
    return render(request,
    "post_list.html",
    {"posts": posts}
    )
@login_required
def post_details(request, pk):
    posts = post.objects.get(pk=pk, published_at__isnull=False)
    return render(request, "post_details.html", {"posts": posts},)

@login_required  
def draft_list(request):
    posts = post.objects.filter(published_at__isnull=True).order_by("-published_at")
    return render(request,
    "draft_list.html",
    {"posts": posts}
    )
    
@login_required  
def draft_details(request, pk):
    posts = post.objects.get(pk=pk, published_at__isnull=True)
    return render(request, "draft_details.html", {"posts": posts},)

def draft_publish(request, pk):
    posts = post.objects.get(pk=pk, published_at__isnull=True)
    posts.published_at = timezone.now()
    posts.save()
    return redirect("post-list")


@login_required
def post_delete(request, pk):
    posts = post.objects.get(pk=pk)
    posts.delete()
    return redirect("post-list")


@login_required
def post_create(request):

    if request.method == "GET":
        form = Postform()
        return render(request, "post_create.html", {"form": form},
        )
        
    else:
        form = Postform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post-list")
        
    return render(
            request,
            "post_create.html",
            {"form":form},
            )

@login_required          
def post_update(request, pk):
    posts = post.objects.get(pk=pk)
    form = Postform(instance=posts)

    if request.method == "POST":
        form = Postform(request.POST, instance=posts)

        if form.is_valid():
            form.save()
            if posts.published_at:
                return redirect("post-details", posts.pk)
            
            else:
                return redirect("draft-details", posts.pk)


        
    return render(
            request,
            "post_create.html",
            {"form":form},
            )



