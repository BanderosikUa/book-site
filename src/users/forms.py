from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Row, Column, Field, ButtonHolder, Submit
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserFormCreate(UserCreationForm, PopRequestMixin,
                           CreateUpdateAjaxMixin):
    # username = forms.CharField(
    #     label='Your Username', widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
    # )
    # email = forms.EmailField(
    #     label='Your Email', widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg'})
    # )
    # password1 = forms.CharField(
    #     label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
    #     min_length=8
    # )
    # password2 = forms.CharField(
    #     label='Repeat your password', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
    #     min_length=8
    # )
    # service_terms = forms.ChoiceField(
    #     label='I agree all statements in',
    #     widget=forms.CheckboxInput(attrs={'class': 'form-check-label"'})
    # )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')



# class CustomUserFormCreate(UserCreationForm):
#     username = forms.CharField(
#         label='username', widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'})
#     )
#     email = forms.EmailField(
#         label='Your Email', widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg'})
#     )
#     password1 = forms.CharField(
#         label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'})
#     )
#     password2 = forms.CharField(
#         label='Repeat your password', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
#     )

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password1', 'password2')
