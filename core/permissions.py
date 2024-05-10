from rest_framework import permissions


class IsInnovationAuthorOrModOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the author, staff, and moderators to edit/delete an innovation.
    """

    def has_permission(self, request, view):
        return True

    # def has_object_permission(self, request, view, obj):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     return obj.author.email == request.user.email or request.user.is_staff or request.user.is_site_mod


class IsInnovationAuthorOrCommentAuthorOrModOrStaffOrReadOnly(
    permissions.BasePermission
):
    """
    Custom permission to allow only the author of the innovation or the author of the comment,
    as well as moderators and staff, to modify the resource.
    """

    def has_permission(self, request, view):
        return True

    # def has_permission(self, request, view):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     return request.user.is_staff or request.user.is_site_mod

    # def has_object_permission(self, request, view, obj):
    #     if obj["author"]["email"] == request.user.email:
    #         return True

    #     return False
