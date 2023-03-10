"""Images URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from Files import views
from rest_framework.schemas import get_schema_view


urlpatterns = [
    path('', get_schema_view(
        title="Images",
        description="Simple API for the Images.",
        version="Test version for recuitement process"
    ), name='openapi-schema'),
    path('images/<int:size>/<int:image_pk>/', views.image_preview_view, name = 'thumbnail-url'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('image/url/<int:image_pk>/', views.imageURLView, name = 'url-list'),
    path('images/', views.UserImageView.as_view()),
    path('exp/link/', views.expiring_link_view, name = 'exp-link'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)