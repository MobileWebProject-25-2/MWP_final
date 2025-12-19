# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 웹 페이지
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    
    # API
    path('api/posts/', views.PostListAPIView.as_view(), name='api_post_list'),
    path('api/posts/<int:pk>/', views.ImageDetailAPIView.as_view(), name='api_post_detail'),
    path('api/guide/<str:item_name>/', views.recycling_guide_by_item, name='api_guide_item'),
    path('api/categories/', views.category_list, name='api_categories'),
]