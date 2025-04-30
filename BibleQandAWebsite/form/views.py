from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .services import get_all_rows
from .forms import QuestionForm, TestimonyForm

def test(request):
    save = get_all_rows("Test sheet")
    return render(request, 'form/test.html', {'save': save})

def home(request):
    return render(request, 'form/home.html')

def question_form(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            time_submitted = datetime.now()
            first_name = form.cleaned_data.get('first_name')
            print(time_submitted, first_name)
            return redirect('questionThanks')
        
    else:
        form = QuestionForm()
    return render(request, 'form/question.html', {'form':form})

def testimony_form(request):
    if request.method == 'POST':
        form = TestimonyForm(request.POST)

        if form.is_valid():
            time_submitted = datetime.now()
            name = form.cleaned_data.get('name')
            print(f'{time_submitted=}, {name=}')
            return redirect('form:home')
        
    else:
        form = TestimonyForm()
    return render(request, 'form/testimony.html', {'form':form})

def question_thanks(request):
    return render(request, 'form/questionThanks.html')

def testimony_thanks(request):
    return render(request, 'form/testimonyThanks.html')

def question_form_redirect(request):
    return HttpResponseRedirect('/form/question/')

def testimony_form_redirect(request):
    return HttpResponseRedirect('/form/testimony/')

def test_redirect(request):
    return HttpResponseRedirect('/test/')