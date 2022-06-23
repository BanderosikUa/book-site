from .forms import CustomUserFormCreate, CustomAuthenticationForm


def add_registration_form(request):
    return {
        'registration_form': CustomUserFormCreate(),
    }

def add_login_form(request):
    return {
        'login_form': CustomAuthenticationForm(),
    }
