from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from news_app import views
from django.contrib.auth import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news_app.urls')),
    path('api/v1/',include("api.urls")),
    path('news-admin/', include('blog_app.urls'), name='news-admin'),
    path("accounts/login/", views.LoginView.as_view(), name="login"),
    path("accounts/logout/", views.LogoutView.as_view(), name="logout"),   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('summernote/', include('django_summernote.urls'))]

