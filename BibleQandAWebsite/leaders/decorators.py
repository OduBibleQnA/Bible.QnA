from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def staff_and_group_required(group_name):
    def check(user):
        if user.is_staff and user.groups.filter(name=group_name).exists():
            return True
        raise PermissionDenied
    return user_passes_test(check)
