from rest_framework.permissions import IsAuthenticated

class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_admin()
    

# class IsAuthor(IsAuthenticated):
#     def has_permission(self, request, view):
#         return request.user.is_author()
    

class IsAuthorOrAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return (request.user.is_author() or request.user.is_admin())
    

class IsPostOwnerOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (request.user.is_admin() or obj.written_by==request.user)