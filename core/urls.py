from django.urls import path

from .views import (CommentCreateAPIView, CommentListAPIView,
                    PostCreateAPIView, PostDeleteAPIView, PostListAPIView,
                    PostUpdateAPIView)

urlpatterns = [
    path('post/new/', PostCreateAPIView.as_view(), name='post-create'),
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('post/<int:pk>/delete/', PostDeleteAPIView.as_view(), name='post-delete'),
    path('post/<int:pk>/update/', PostUpdateAPIView.as_view(), name='post-update'),
    path('post/<int:post_pk>/newcomment/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('post/<int:post_pk>/comments/', CommentListAPIView.as_view(), name='comment-list'),
]