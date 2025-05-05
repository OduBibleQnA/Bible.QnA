from django import forms
from .models import Question, Testimony
import re


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['first_name', 'question']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your First Name'
            }),
            'question': forms.Textarea(attrs={
                'class': 'form-control auto-resize',
                'placeholder': 'Your Question',
                'style': 'height: 100px; resize: none; overflow:hidden;'
            }),
        }


class TestimonyForm(forms.ModelForm):
    class Meta:
        model = Testimony
        fields = ['name', 'shortened_testimony', 'on_camera', 'contact_method', 'encrypted_contact_detail']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'shortened_testimony': forms.Textarea(attrs={
                'class': 'form-control auto-resize',
                'id': 'id_shortened_testimony',
                'placeholder': ' ',
                'style': 'height: 300px; resize: none; overflow: hidden;'
            }),
            'on_camera': forms.Select(choices=[('', 'Choose...'), ('true', 'Yes'), ('false', 'No')],
                                      attrs={'class': 'form-select'}),
            'contact_method': forms.Select(attrs={'class': 'form-select'}),
            'encrypted_contact_detail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
        }

    def clean_on_camera(self):
        val = self.cleaned_data['on_camera']
        return val == 'true' if isinstance(val, str) else val

    def clean_shortened_testimony(self):
        value = self.cleaned_data.get('shortened_testimony', '')
        words = len(value.strip().split())

        if words < 50:
            raise forms.ValidationError("Please write at least 50 words.")
        if words > 175:
            raise forms.ValidationError("Please keep your response under 175 words.")
        return value

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get('contact_method')
        detail = cleaned_data.get('contact_detail')

        if not method or not detail:
            return cleaned_data

        if method == 'phone':
            if not re.fullmatch(r'^\+?\d{7,15}$', detail):
                self.add_error('contact_detail', 'Enter a valid phone number (7–15 digits, optional +).')

        elif method == 'email':
            if not re.fullmatch(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', detail):
                self.add_error('contact_detail', 'Enter a valid email address.')

        elif method == 'instagram':
            detail = detail.lstrip('@')
            cleaned_data['contact_detail'] = detail
            if not re.fullmatch(r'^[A-Za-z0-9._]{1,30}$', detail):
                self.add_error('contact_detail', 'Enter a valid Instagram handle (no spaces, up to 30 characters).')

        return cleaned_data
