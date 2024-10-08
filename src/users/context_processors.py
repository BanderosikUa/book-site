from .forms import UserFormCreate, CustomAuthenticationForm
from django.contrib.auth.forms import PasswordResetForm


def add_registration_form(request):
    return {
        'registration_form': UserFormCreate(),
    }


def add_login_form(request):
    return {
        'login_form': CustomAuthenticationForm(),
    }


def send_reset_email_form(request):
    return {
        'send_reset_email_form': PasswordResetForm(),
    }
