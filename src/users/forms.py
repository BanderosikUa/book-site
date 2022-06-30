from attr import attrs
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Row, Column, Field, ButtonHolder, Submit

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from .models import CustomUser


class CustomUserFormCreate(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CustomUserFormCreate, self).__init__(*args, **kwargs)
    
    username = forms.CharField(
        label='Your Username', widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
    )
    email = forms.EmailField(
        label='Your Email', widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg'})
    )
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
        min_length=8
    )
    password2 = forms.CharField(
        label='Repeat your password', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
        min_length=8
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label='')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def singup(self, request, user):
        user.username = self.cleaned_data['first_name'] + ' ' + self.cleaned_data['last_name']
        user.avatar = self.cleaned_data['picture']
        user.save()


class CustomAuthenticationForm(AuthenticationForm):
    prefix = 'login'

    username = forms.CharField(
        label='Your Username', widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
    )
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class ChangePasswordForm(PasswordChangeForm):
    
    class Meta:
        model = CustomUser
