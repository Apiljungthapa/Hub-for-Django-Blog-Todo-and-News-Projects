from django.views.generic import ListView,TemplateView,View,DetailView
from news_app.models import Post
from django.utils import timezone
from datetime import timedelta
from news_app.models import Category
from django.shortcuts import render,redirect
from news_app.models import Tag
from news_app.forms import contactForm,CommentForm,NewsLetterForm
from django.contrib import messages
from django.http import JsonResponse



class HomeView(ListView):
    model = Post
    template_name = "aznews/home.html"
    context_object_name = "posts"
    queryset=Post.objects.filter(published_at__isnull=False, status="active")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feature_post"] = Post.objects.filter(published_at__isnull=False, status="active").order_by("-published_at").first()
        context["featured_posts"] = Post.objects.filter(published_at__isnull=False, status="active").order_by("-published_at")[1:4]

        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] = Post.objects.filter(published_at__isnull=False, status="active", published_at__gte=one_week_ago).order_by("-published_at")[:7]
        context["recent_posts"] = Post.objects.filter(published_at__isnull=False, status="active").order_by("-published_at")[:7]

        

        return context

class AboutView(TemplateView):
    template_name = "aznews/about.html"

    

class ContactView(View):
    template_name = "aznews/contact.html"
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = contactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"form submitted successfully ! we will contact you soon ")
            return redirect("contact")

        else:
            print(form.errors) 
            messages.error(request, "Form submission failed. Please correct the errors.")
            return render(request,self.template_name,{"form":form},)


class PostView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=False, status="active").order_by("-published_at")
    paginate_by = 1
    
class PostByCategoryView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=False, status="active").order_by("-published_at")
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False,
            status="active",
            category__id=self.kwargs.get("category_id"),
            ).order_by("-published_at")

class PostByTagView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=False, status="active").order_by("-published_at")
    paginate_by = 1

    def get_queryset(self):
        tag_id = self.kwargs.get("tag_id")
        return Post.objects.filter(
            published_at__isnull=False,
            status="active",
            tag__id=tag_id,
        ).order_by("-published_at")
    
    # def get_queryset(self):
    #     tag__id = self.kwargs.get("tag_id"),
    #     return Post.objects.filter(
    #         published_at__isnull=False,
    #         status="active",
    #         tag__id=tag__id,
    #     ).order_by("-published_at")

   


class PostDetailView(DetailView):
    model = Post
    template_name = "aznews/detail/detail.html"
    context_object_name = "post"  # Use singular name for the object

    def get_queryset(self):
        return Post.objects.filter(published_at__isnull=False, status="active")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj=self.get_object()
        
        context['previous_post'] = (
            Post.objects.filter(
                published_at__isnull=False, status="active", id__lt=obj.id)
                .order_by('-id')
                .first()
        )

        context['next_post'] = (
            Post.objects.filter(
                published_at__isnull=False, status="active", id__gt=obj.id)
                .order_by('id')
                .first()
        )

        return context


class CommentView(View):

    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST["post"]
            form.save()
            return redirect("post-detail", pk=post_id)
        else:
            post_id = request.POST["post"]
            post = Post.objects.get(pk=post_id)
            return render(
                request,
                "aznews/detail/detail.html",
                {"post": post, "form": form},
            )



class NewsletterView(View):

    def post(self, request):

        is_ajax = request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":  # ajax request
            form = NewsLetterForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {
                        "success": True,
                        "message": "Successfully subscribed to the newsletter.",
                    },
                    status=201,
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Cannot subscribe to the newsletter.",
                    },
                    status=400,
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot process. Must be an AJAX XMLHttpRequest",
                },
                status=400,
            )



from django.db.models import Q  #it is for or case
from django.core.paginator import Paginator, PageNotAnInteger

class PostSearchList(View):
    template_name = "aznews/list/list.html"
    
    def get(self, request, *args, **kwargs):
        query = request.GET["query"]  #it can be case sensitive or in sensitive
        post_list = Post.objects.filter(
            (Q(title__icontains=query) | Q(content__icontains=query))
            & Q(status="active")
            & Q(published_at__isnull=False)
        ).order_by("-published_at")

        page = request.GET.get("page", 1)
        paginate_by = 1
        paginator = Paginator(post_list, paginate_by)

        try:
            posts = paginator.page(page)
        
        except PageNotAnInteger:
            posts = paginator.page(1)


        return render(request,
            self.template_name,
            {"page_obj":posts}
        )
        

class PreSearchList(View):
    template_name = "aznews/list/list.html"
    
    def get(self, request, *args, **kwargs):
        j_query = request.GET["j_query"]  #it can be case sensitive or in sensitive
        post_list = Post.objects.filter(
            (Q(title__icontains=j_query) | Q(content__icontains=j_query))
            & Q(status="active")
            & Q(published_at__isnull=False)
        ).order_by("-published_at")

        return render(request,
            self.template_name,
            {"page_obj":posts}
        )
