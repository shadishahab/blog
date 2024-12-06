from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from core.models import Post


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()
    

class IsAuthorOrAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_author() or request.user.is_admin())
    

class IsReaderOrAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_reader() or request.user.is_admin())
    

class IsPostOwnerOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (request.user.is_admin() or obj.written_by==request.user)
    

class IsCommentPostOwnerOrAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        post_pk = view.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)
        return request.user.is_authenticated and (request.user.is_admin() or post.written_by==request.user)