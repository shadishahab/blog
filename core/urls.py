from django.urls import path
from .views import PostCreateAPIView, PostListAPIView, PostDeleteAPIView, PostUpdateAPIView

urlpatterns = [
    path('post/new/', PostCreateAPIView.as_view(), name='post-create'),
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('post/delete/<int:pk>', PostDeleteAPIView.as_view(), name='post-delete'),
    path('post/update/<int:pk>', PostUpdateAPIView.as_view(), name='post-update'),
]