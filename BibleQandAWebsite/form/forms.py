from django import forms
import re

class QuestionForm(forms.Form):
    first_name = forms.CharField(
        label="Enter Your First Name",
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your First Name',
        })
    )
    question = forms.CharField(
        label="Your Question",
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your Question',
            'style': 'height: 100px;'
        })
    )


class TestimonyForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    shortened_testimony = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'id_shortened_testimony', 'placeholder': ' ', 'style': 'height: 300px; resize :none;'}))
    # yes_or_no = forms.ChoiceField(
    #     choices=[('yes', 'Yes'), ('no', 'No')],
    #     widget=forms.Select(attrs={'class': 'form-select'})
    # )

    yes_or_no = forms.TypedChoiceField(
        choices=[('', 'Choose...'), ('true', 'Yes'), ('false', 'No')],
        coerce=lambda x: x == 'true',
        empty_value=None,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    contact_method = forms.ChoiceField(
        choices=[('', 'Choose...'), ('instagram', 'Instagram'), ('phone', 'Phone'), ('email', 'Email')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    contact_detail = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}))

    def clean_yes_or_no(self):
        value = self.cleaned_data.get('yes_or_no')
        if value is None:
            raise forms.ValidationError("Please select Yes or No.")
        return value    

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

        # Phone
        if method == 'phone':
            if not re.fullmatch(r'^\+?\d{7,15}$', detail):
                self.add_error('contact_detail', 'Enter a valid phone number (7–15 digits, optional +).')

        # Email
        elif method == 'email':
            if not re.fullmatch(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', detail):    
                self.add_error('contact_detail', 'Enter a valid email address.')

        # Instagram
        elif method == 'instagram':
            detail = detail.lstrip('@')
            cleaned_data['contact_detail'] = detail
            if not re.fullmatch(r'^[A-Za-z0-9._]{1,30}$', detail):
                self.add_error('contact_detail', 'Enter a valid Instagram handle (no spaces, up to 30 characters).')

        return cleaned_data
