from django.contrib.auth import views as reset
from django.urls import path, include, reverse_lazy

password_reset_urlpatterns = [
    path('reset-password/', reset.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        html_email_template_name='registration/password_reset_email.html',  # THIS is key
        subject_template_name='registration/password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done'),
    ), name='password_reset'),
    
    path("reset-password/done/", reset.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_done"),

    path('<uidb64>/<token>/', reset.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('done/', reset.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]

urlpatterns = [
    path('login/', reset.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.CustomLogoutView.as_view(), name='logout'),
    path('logout/', reset.LogoutView.as_view(), name='logout'),

    # Password reset flow
    path('reset/', include(password_reset_urlpatterns)),

    # Password change (for logged-in users)
    path('password-change/', reset.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password-change/done/', reset.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
]
