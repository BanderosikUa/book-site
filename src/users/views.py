from django.shortcuts import render
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView
from .forms import CustomUserFormCreate


class RegistrationView(BSModalCreateView):
    form_class = CustomUserFormCreate
    template_name = 'registration.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('')
