from django.contrib.auth.models import Group

def user_groups(request):
    if request.user.is_authenticated:
        return {
            "is_podcaster": request.user.groups.filter(name="podcasters").exists()
        }
    return {"is_podcaster": False}
