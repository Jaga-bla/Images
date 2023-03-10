from rest_framework import permissions

class HasThumbnailPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    permission_thumbnail_size = ""
    
    def __init__(self, permission_thumbnail_size):
        super().__init__()
        self.permission_thumbnail_size = permission_thumbnail_size

    def __call__(self):
        return self
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        for thumbnail_size in request.user.profile.permission.thumbnail_option.all():
            if thumbnail_size.size == self.permission_thumbnail_size:
                return True
        return False
    

class HasExpirationLinkPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.profile.permission.exp_link:
            return True
        return False
    
class HasOriginalLinkPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.profile.permission.org_link:
            return True
        return False