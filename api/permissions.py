from rest_framework import permissions

class AllowPostOnlyForAuthenticated(permissions.BasePermission):
    """
    Custom permission class to allow only authenticated users
    to make POST requests
    """
    
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return request.user.is_authenticated