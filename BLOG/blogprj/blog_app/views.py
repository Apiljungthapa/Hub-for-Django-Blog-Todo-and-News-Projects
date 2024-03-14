from django.shortcuts import render,redirect
from blog_app.models import post
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import Postform
from django.views.generic import ListView,DetailView,View,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy



#from class
class PostListView(ListView):
    model = post
    template_name = "post_list.html"
    context_object_name = "posts"
    # queryset = post.objects.filter(published_at__isnull=False).order_by("-published_at")

    def get_queryset(self):
        queryset = post.objects.filter(published_at__isnull=False).order_by("-published_at")
        return queryset



# @login_required
# def post_details(request, pk):
#     posts = post.objects.get(pk=pk, published_at__isnull=False)
#     return render(request, "post_details.html", {"posts": posts},)


class PostDetailView(DetailView):
    model = post
    template_name = "post_details.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=False)
        return queryset



class DraftListView(LoginRequiredMixin, ListView):
    model = post
    template_name = "draft_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = post.objects.filter(published_at__isnull=True)
        return queryset


class DraftDetailView(DetailView):
    model = post
    template_name = "draft_details.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=True)
        return queryset



class DraftPublishView(LoginRequiredMixin, ListView):
    def get(self, request, pk):
        posts = post.objects.get(pk=pk, published_at__isnull=True)
        posts.published_at = timezone.now()
        posts.save()
        return redirect("post-list")

class DeleteView(LoginRequiredMixin, ListView):
    def get(self, request, pk):
        posts = post.objects.get(pk=pk)
        posts.delete()
        return redirect("post-list")




class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    template_name = "post_create.html"
    form_class = Postform
    success_url = reverse_lazy("draft-list")
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)





# @login_required
# def post_create(request):

#     if request.method == "GET":
#         form = Postform()
#         return render(request, "post_create.html", {"form": form},
#         )
        
#     else:
#         form = Postform(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect("post-list")
        
#     return render(
#             request,
# #             "post_create.html",
# #             {"form":form},
# #             )

# @login_required          
# def post_update(request, pk):
#     posts = post.objects.get(pk=pk)
#     form = Postform(instance=posts)

#     if request.method == "POST":
#         form = Postform(request.POST, instance=posts)

#         if form.is_valid():
#             form.save()
#             if posts.published_at:
#                 return redirect("post-details", posts.pk)
            
#             else:
#                 return redirect("draft-details", posts.pk)


        
#     return render(
#             request,
#             "post_create.html",
#             {"form":form},
#             )


class PostupdateView(LoginRequiredMixin, UpdateView):
    model = post
    template_name = "post_create.html"
    form_class = Postform
    
    def get_success_url(self):
        post = self.get_object()
        
        if post.published_at:
        
            return reverse_lazy("post-details", kwargs={"pk": post.pk})
            
        else:
            return reverse_lazy("draft-details", kwargs={"pk": post.pk})


