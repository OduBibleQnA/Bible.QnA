from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .utils.votd import get_votd_html
from .forms import QuestionForm, TestimonyForm
from .models import Testimony

def home(request):
    votd_html = get_votd_html()  # Fetch cached or fresh VOTD
    return render(request, 'form/home.html', {'votd_html': votd_html})


def question_form(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('form:questionThanks')
    else:
        form = QuestionForm()
    return render(request, 'form/question.html', {'form': form})


def testimony_form(request):
    if request.method == 'POST':
        form = TestimonyForm(request.POST)
        if form.is_valid():
            testimony = Testimony(
                name=form.cleaned_data['name'],
                shortened_testimony=form.cleaned_data['shortened_testimony'],
                on_camera=form.cleaned_data['on_camera'],
                contact_method=form.cleaned_data['encrypted_contact_detail'],
            )
            testimony.set_contact_detail(form.cleaned_data['encrypted_contact_detail'])
            testimony.save()
            return redirect('form:testimonyThanks')
    else:
        form = TestimonyForm()
    return render(request, 'form/testimony.html', {'form': form})


def question_thanks(request):
    return render(request, 'form/questionThanks.html')

def testimony_thanks(request):
    return render(request, 'form/testimonyThanks.html')

def question_form_redirect(request):
    return HttpResponseRedirect('/form/question/')

def testimony_form_redirect(request):
    return HttpResponseRedirect('/form/testimony/')
