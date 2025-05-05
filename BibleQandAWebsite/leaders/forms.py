from django import forms
from form.models import Question
from django.utils.timezone import now

class QuestionStaffForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['answered', 'answer_medium', 'answer_date']
        widgets = {
            'answered': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'answer_date': forms.DateInput(
                attrs={'type': 'date', 'min': now().date().isoformat(), 'class': 'form-control'}
            ),
            'answer_medium': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_answer_date(self):
        answer_date = self.cleaned_data.get('answer_date')
        if answer_date and answer_date < now().date():
            raise forms.ValidationError("The answer date must be today or in the future.")
        return answer_date
