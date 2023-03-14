from django.urls import path
from . import views


urlpatterns = [
    path('', views.UserImageView.as_view(), name = 'image-list'),    
    path('url/<int:image_pk>/', views.ImageUrlView.as_view(), name = 'url-list'),
    path('thumbnail/<int:size>/<int:image_pk>/', views.image_thumbnail_view, name = 'thumbnail-url'),
    path('exp/link/<int:image_pk>/', views.image_exp_link_view, name = 'exp-link'),
    path('<int:image_pk>/', views.image_org_link_view, name = 'org-link'),
]
