from django.http import Http404
from django.core.exceptions import PermissionDenied

def check_permissions(function):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name="professor").exists():
            return function(request, *args, **kwargs)
        raise PermissionDenied()

    return wrapper