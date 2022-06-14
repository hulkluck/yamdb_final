from rest_framework.permissions import BasePermission, SAFE_METHODS


class GetOrAuthorOrAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        return (request.method == 'GET'
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method == 'GET'
                or request.user == obj.author
                or request.user.is_moderator
                or request.user.is_admin)


class AuthorOrModeratorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author
                or request.user.is_moderator
                or request.user.is_admin)


class DetailForAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.is_staff
                     or request.user.is_admin))


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)
