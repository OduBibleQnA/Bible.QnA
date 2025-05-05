from django.urls import path, include
from . import views

app_name = "leaders"

youtube_urlpatterns = [
    path('dashboard/', views.youtube_dashboard, name='youtube_dashboard'),
    path('upload/', views.youtube_upload, name='youtube_upload'),
    path('auth/start/', views.start_auth, name='youtube_auth_start'),
    path('auth/callback/', views.oauth2_callback, name='youtube_auth_callback'),
    path('analytics/', views.youtube_analytics, name='youtube_analytics'),
    path('oauth2callback/', views.youtube_oauth2callback, name='youtube-oauth2callback'),
]

spotify_urlpatterns = [
    path('spotify/', views.spotify_redirect, name='spotify_redirect'),
    # Add more leader-specific views here
]

leader_urlpatterns = [
    path('questions/', views.view_questions, name='view_questions'),
    path('questions/<int:pk>/mark/', views.mark_question, name='mark_question'),
    path('questions/archived/', views.archived_questions, name='archived_questions'),
    path('questions/<int:pk>/unarchive/', views.unarchive_question, name='unarchive_question'),
]

podcast_urlpatterns = [
    path('testimonies/', views.pending_testimonies, name='testimonies_pending'),
    path('testimonies/approve/<int:pk>/', views.approve_testimony, name='approve_testimony'),
    path('testimonies/archive/<int:pk>/', views.archive_testimony, name='archive_testimony'),
    path('testimonies/delete/<int:pk>/', views.delete_testimony, name='delete_testimony'),
    path('testimonies/archived/', views.archived_testimonies, name='archived_testimonies'),
    path('testimonies/<int:pk>/unarchive/', views.unarchive_testimony, name='unarchive_testimony'),
]

urlpatterns = [
    path('youtube/', include((youtube_urlpatterns, 'youtube'), namespace="youtube")),
    path('spotify/', include((spotify_urlpatterns, 'spotify'), namespace='spotify')),
    path('podcast/', include((podcast_urlpatterns, 'podcast'), namespace='podcast')),
    path('', include((leader_urlpatterns, 'core'), namespace='core')),
]