from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator

from ..forms import CustomAuthenticationForm, UserFormCreate


def email_send_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            token_generator = default_token_generator
            extra_context = {'sent_url': request.POST.get('url')}
            opts = {
                "use_https": request.is_secure(),
                "token_generator": token_generator,
                "from_email": None,
                "email_template_name": "password_reset/password_reset_email.html",
                "subject_template_name": "registration/password_reset_subject.txt",
                "request": request,
                "html_email_template_name": None,
                "extra_email_context": extra_context,
            }
            form.save(**opts)
            return JsonResponse({'error': False, 'success_message': 'Email was send!'})
        else:
            rendered_template = render_to_string(
                'password_reset/send_email_for_reset.html',
                {'send_reset_email_form': form},
                request=request)
            return JsonResponse({'error': True, 'form': rendered_template})


def reset_password_confirm_view(request):
    pass


def registration_validation_view(request):
    if request.method == 'POST':
        form = UserFormCreate(request.POST)
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
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            rendered_template = render_to_string('login.html', {'login_form': form},
                                                 request=request)
            return JsonResponse({'error': True, 'form': rendered_template})


def login_view(request):
    return redirect('#LoginModal')
