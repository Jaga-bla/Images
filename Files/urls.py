from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.UserImageView.as_view()),    
    path('url/<int:image_pk>/', views.ImageUrlView.as_view(), name = 'url-list'),
    path('thumbnail/<int:size>/<int:image_pk>/', views.image_thumbnail_view, name = 'thumbnail-url'),
    path('exp/link/<int:image_pk>/', views.image_exp_link_view, name = 'exp-link'),
    path('<int:image_pk>/', views.image_org_link_view, name = 'org-link'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
