from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from lib.pagination import CustomPagination
from users.permissions import IsAuthorOrAdmin, IsAdmin, IsPostOwnerOrAdmin
from .serializers import PostWriteSerializer, PostReadSerializer, PostUpdateSerializer
from .models import Post

class PostCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthorOrAdmin]
    queryset = Post.objects.all()
    serializer_class = PostWriteSerializer


class PostListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Post.objects.all()
    serializer_class = PostReadSerializer


class PostDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Post.objects.all()
    serializer_class = PostWriteSerializer


class PostUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsPostOwnerOrAdmin]
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer