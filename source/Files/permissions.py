from rest_framework import permissions


def has_thumbnail_permission(request, size):
    for thumnail_option in request.user.profile.permission.thumbnail_option.all():
        if thumnail_option.size == size:
            return True
    return False

def custom_thumnail_permission(request):
    for thumnail_option in request.user.profile.permission.thumbnail_option.all():
        if thumnail_option.size != 200 and thumnail_option.size !=400:
            return thumnail_option.size
    return False

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