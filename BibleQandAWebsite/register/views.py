from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

class CustomPasswordResetView(auth_views.PasswordResetView):
    email_template_name = None  # Don't use default
    success_url = reverse_lazy('auth:password_reset_done')
    form_class = PasswordResetForm
    template_name = 'auth/password_reset_form.html'

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        UserModel = get_user_model()
        for user in UserModel._default_manager.filter(email__iexact=email, is_active=True):
            context = {
                'email': user.email,
                'domain': self.request.get_host(),
                'site_name': 'ODU Bible Q&A',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if self.request.is_secure() else 'http',
            }

            subject = render_to_string('auth/password_reset_subject.txt', context).strip()
            html_body = render_to_string('auth/password_reset_email.html', context)
            text_body = render_to_string('auth/password_reset_email.txt', context)

            email_message = EmailMultiAlternatives(subject, text_body, None, [user.email])
            email_message.attach_alternative(html_body, "text/html")
            email_message.send()

        return super().form_valid(form)

class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('form:home')


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('register:password_reset_done')

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('register:password_reset_complete')

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

class CustomPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('register:password_change_done')

class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'
