from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissões customizadas :.
    """

    def has_object_permission(self, request, view, obj):
        # Permissões de leitura permitidas para:
        # GET, HEAD ou OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Alteração do filme permitida somente para o criador
        return obj.creator == request.user