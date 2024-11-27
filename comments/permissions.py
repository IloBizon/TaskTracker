from rest_framework.permissions import BasePermission

from comments.models import Comment


class UserIsCommentAuthorOrStaff(BasePermission):
    SAFE_METHODS = ['GET']
    def has_object_permission(self, request, view, obj):
        if request.method in self.SAFE_METHODS or request.user.id == obj.author.id:
            return True
        return False