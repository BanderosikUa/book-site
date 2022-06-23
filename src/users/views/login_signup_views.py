from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.contrib import messages

from ..forms import CustomAuthenticationForm, CustomUserFormCreate


def registration_validation_view(request):
    if request.method == 'POST':
        form = CustomUserFormCreate(request.POST)
        print(form)
        if not form.is_valid():
            rendered_template = render_to_string('registration.html',
                                                 {'registration_form': form},
                                                 request=request)
            return JsonResponse({'error': True, 'form': rendered_template})
        else:
            user = form.save()
            messages.success(request, "Registration successful.")
            return JsonResponse({'error': False})


def login_validation_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.META['HTTP_REFERER'])
        rendered_template = render_to_string('login.html', {'login_form': form},
                                             request=request)
        return JsonResponse({'error': True, 'form': rendered_template})


def login_view(request):
    print(request.path)
    return redirect('#LoginModal')
