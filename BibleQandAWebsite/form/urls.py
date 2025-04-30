from django.urls import path
from . import views


app_name = "form"
urlpatterns = [
    path('', views.home, name='home'),
    path('form/question', views.question_form_redirect, name='questionForm'),
    path('form/question/', views.question_form, name='questionForm'),
    path('form/testimony', views.testimony_form_redirect, name='testimonyForm'),
    path('form/testimony/', views.testimony_form, name='testimonyForm'),
    path('test', views.test_redirect, name='test'),
    path('test/', views.test, name='test'),
    path('form/question/thanks/', views.question_thanks, name='questionThanks'),
    path('form/testimony/thanks/', views.testimony_thanks, name='testimonyThanks'),
]