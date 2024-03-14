from django.urls import path
from blog_app import views 

urlpatterns = [
    path('', views.PostListView.as_view(), name="post-list"),
    path("post_details/<int:pk>/", views.PostDetailView.as_view(), name="post-details"),
    path("draft-list/", views.DraftListView.as_view(), name="draft-list"),
    path("draft_details/<int:pk>/", views.DraftDetailView.as_view(), name="draft-details"),
    path("draft_publish/<int:pk>/", views.DraftPublishView.as_view(), name="draft-publish"),
    path("post-delete/<int:pk>/", views.DeleteView.as_view(), name="post-delete"),
    path("post-create/", views.PostCreateView.as_view(), name="post-create"),
    path("post-update/<int:pk>/", views.PostupdateView.as_view(), name="post-update"),

]
