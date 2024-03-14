# from django.shortcuts import render,redirect
# from blog_app.models import post
# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from .forms import Postform
# from django.views.generic import ListView,DetailView,View,CreateView,UpdateView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy
# from typing import Any




# #from class
# class PostListView(ListView):
#     model = post
#     template_name = "post_list.html"
#     context_object_name = "posts"
#     # queryset = post.objects.filter(published_at__isnull=False).order_by("-published_at")

#     def get_queryset(self):
#         queryset = post.objects.filter(published_at__isnull=False).order_by("-published_at")
#         return queryset



# # @login_required
# # def post_details(request, pk):
# #     posts = post.objects.get(pk=pk, published_at__isnull=False)
# #     return render(request, "post_details.html", {"posts": posts},)


# class PostDetailView(DetailView):
#     model = post
#     template_name = "post_details.html"
#     context_object_name = "posts"

#     def get_queryset(self):
#         queryset = post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=False)
#         return queryset



# class DraftListView(LoginRequiredMixin, ListView):
#     model = post
#     template_name = "draft_list.html"
#     context_object_name = "posts"

#     def get_queryset(self):
#         queryset = post.objects.filter(published_at__isnull=True)
#         return queryset


# class DraftDetailView(DetailView):
#     model = post
#     template_name = "draft_details.html"
#     context_object_name = "posts"

#     def get_queryset(self):
#         queryset = post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=True)
#         return queryset




# class DraftPublishView(LoginRequiredMixin, ListView):
#     def get(self, request, pk):
#         posts = post.objects.get(pk=pk, published_at__isnull=True)
#         posts.published_at = timezone.now()
#         posts.save()
#         return redirect("post-list")

# class DeleteView(LoginRequiredMixin, ListView):
#     def get(self, request, pk):
#         posts = post.objects.get(pk=pk)
#         posts.delete()
#         return redirect("post-list")




# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = post
#     template_name = "post_create.html"
#     form_class = Postform
#     success_url = reverse_lazy("draft-list")
    
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)





# # @login_required
# # def post_create(request):

# #     if request.method == "GET":
# #         form = Postform()
# #         return render(request, "post_create.html", {"form": form},
# #         )
        
# #     else:
# #         form = Postform(request.POST)
# #         if form.is_valid():
# #             post = form.save(commit=False)
# #             post.author = request.user
# #             post.save()
# #             return redirect("post-list")
        
# #     return render(
# #             request,
# # #             "post_create.html",
# # #             {"form":form},
# # #             )

# # @login_required          
# # def post_update(request, pk):
# #     posts = post.objects.get(pk=pk)
# #     form = Postform(instance=posts)

# #     if request.method == "POST":
# #         form = Postform(request.POST, instance=posts)

# #         if form.is_valid():
# #             form.save()
# #             if posts.published_at:
# #                 return redirect("post-details", posts.pk)
            
# #             else:
# #                 return redirect("draft-details", posts.pk)


        
# #     return render(
# #             request,
# #             "post_create.html",
# #             {"form":form},
# #             )


# class PostupdateView(LoginRequiredMixin, UpdateView):
#     model = post
#     template_name = "post_create.html"
#     form_class = Postform
    
#     def get_success_url(self):
#         post = self.get_object()
        
#         if post.published_at:
        
#             return reverse_lazy("post-details", kwargs={"pk": post.pk})
            
#         else:
#             return reverse_lazy("draft-details", kwargs={"pk": post.pk})



### new code

from typing import Any
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from blog_app.forms import CategoryForm, PostForm, TagForm
from news_app.models import Post, Tag, Category
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy



# function based views
# 80 - 90 % => CRUD
# class based views


class PostListView(ListView):
    model = Post
    template_name = "news_admin/post_list.html"
    # queryset = Post.objects.filter(published_at__isnull=False).order_by("-published_at")
    context_object_name = "posts"

    def get_queryset(self):
        queryset = Post.objects.filter(published_at__isnull=False).order_by(
            "-published_at"
        )
        return queryset


class PostDetailView(DetailView):
    model = Post
    template_name = "news_admin/post_details.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=False)
        return queryset


class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "news_admin/draft_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = Post.objects.filter(published_at__isnull=True)
        return queryset


class DraftDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "news_admin/draft_details.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=True)
        return queryset


class DraftPublishView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk, published_at__isnull=True)
        post.published_at = timezone.now()
        post.save()
        return redirect("news_admin:post-list")
        
# DraftListView
# DraftDetailView
# DraftPublishView
# PostCreateView

class DeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect("news_admin:post-list")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "admin_lte/post_create.html"
    # template_name = "news_admin/post_create.html"
    form_class = PostForm
    success_url = reverse_lazy("news_admin:all-post-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = "Post"
        return context


class PostupdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "news_admin/post_create.html"
    form_class = PostForm
    success_url = reverse_lazy("news_admin:post-list")

    def get_success_url(self):
        post = self.get_object()
        if post.published_at:
            return reverse_lazy("news_admin:post-detail", kwargs={"pk": post.pk})
        else:
            return reverse_lazy("news_admin:draft-detail", kwargs={"pk": post.pk})

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = "Post"
        return context


# class PostUpdateView(LoginRequiredMixin, View):
#     def get(self, request, pk):
#         post = Post.objects.get(pk=pk)
#         form = PostForm(instance=post)
#         return render(
#             request,
#             "post_create.html",
#             {"form": form},
#         )

#     def post(self, request, pk):
#         post = Post.objects.get(pk=pk)
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save()
#             if post.published_at:
#                 return redirect("news_admin:post-detail", post.pk)
#             else:
#                 return redirect("news_admin:draft-detail", post.pk)
#         return render(
#             request,
#             "post_create.html",
#             {"form": form},
#         )


# @login_required
# def post_update(request, pk):
#     post = Post.objects.get(pk=pk)
#     form = PostForm(instance=post)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save()
#             if post.published_at:
#                 return redirect("news_admin:post-detail", post.pk)
#             else:
#                 return redirect("news_admin:draft-detail", post.pk)

#     return render(
#         request,
#         "news_admin/post_create.html",
#         {"form": form},
#     )



################# Admin Panel #######################

class AllPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "admin_lte/post_list.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = "Post"
        return context


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    template_name = "admin_lte/tag_create.html"
    form_class = TagForm
    success_url = reverse_lazy("news_admin:tag-list")

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = "Tag"
        return context


class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = "admin_lte/tag_list.html"
    context_object_name = "tags"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = "Tag"
        return context


class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    template_name = "admin_lte/tag_create.html"
    form_class = TagForm
    success_url = reverse_lazy("news_admin:tag-list")

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = "Tag"
        return context


class TagDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Tag.objects.get(pk=pk)
        post.delete()
        return redirect("news_admin:tag-list")


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = "admin_lte/category_create.html"
    form_class = CategoryForm
    success_url = reverse_lazy("news_admin:category-list")

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = "Category"
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "admin_lte/category_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = "Category"
        return context


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = "admin_lte/category_create.html"
    form_class = CategoryForm
    success_url = reverse_lazy("news_admin:category-list")

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = "Category"
        return context


class CategoryDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Category.objects.get(pk=pk)
        post.delete()
        return redirect("news_admin:category-list")

