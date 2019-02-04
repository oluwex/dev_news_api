from rest_framework.permissions import BasePermission

class IsAuthor(BasePermission):

    message = "You are not authorized to modify this article."

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user.profile