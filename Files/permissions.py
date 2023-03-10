from rest_framework import permissions

class HasExpirationLinkPermission(permissions.BasePermission):
    """
    View permission to only allow owners with specific permission 
    access the view.
    """

    def has_permission(self, request, view):
        if request.user.profile.permission.exp_link:
            return True
        return False
    
class HasOriginalLinkPermission(permissions.BasePermission):
    """
    View permission to only allow owners with specific permission 
    access the view.
    """

    def has_permission(self, request, view):
        if request.user.profile.permission.org_link:
            return True
        return False