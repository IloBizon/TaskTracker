from rest_framework.permissions import BasePermission
from tasks.service import user_in_task

class UserInTaskOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if user_in_task(obj, request.user):
            return True
        else:
            return False