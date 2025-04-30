from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

# Create your views here.
@login_required(login_url='auth/login/')
def home(request):
    ...

# https://creators.spotify.com/pod/dashboard/episode/wizard
@ staff_member_required(login_url='auth/login/')
def upload_spotify(request):
    return render(request, )
