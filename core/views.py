from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.permissions import (IsAdmin, IsAuthorOrAdmin,
                               IsCommentPostOwnerOrAdmin, IsPostOwnerOrAdmin,
                               IsReaderOrAdmin)
from utils.pagination import CustomPagination

from .filters import PostFilter
from .models import Comment, Post
from .serializers import (CommentReadSerializer, CommentWriteSerializer,
                          PostReadSerializer, PostUpdateSerializer,
                          PostWriteSerializer)


class PostCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthorOrAdmin]
    queryset = Post.objects.all()
    serializer_class = PostWriteSerializer


class PostListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostReadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter


class PostDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Post.objects.all()
    serializer_class = PostWriteSerializer


class PostUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsPostOwnerOrAdmin]
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer


class CommentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsReaderOrAdmin]
    queryset = Comment.objects.all()
    serializer_class = CommentWriteSerializer

    def perform_create(self, serializer):
        post_pk = self.kwargs['post_pk']
        post = get_object_or_404(Post, pk=post_pk)
        serializer.save(post=post)


class CommentListAPIView(generics.ListAPIView):
    permission_classes = [IsCommentPostOwnerOrAdmin]
    serializer_class = CommentReadSerializer
    
    def get_queryset(self):
        post_pk = self.kwargs['post_pk']
        post = get_object_or_404(Post, pk=post_pk)
        return Comment.objects.filter(post=post)