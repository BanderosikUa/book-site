from django.http import Http404
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView, FormView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import *
from ..models import CustomUser


class InformationSettingsView(UpdateView, LoginRequiredMixin):
    model = CustomUser
    template_name = 'users/settings/information.html'
    fields = ['avatar', 'username', 'email']

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return self.model.objects.get(pk=user_id)

    def get_success_url(self):
        user_id = self.kwargs.get('user_id')
        return reverse_lazy('profile-settings-information', kwargs={'user_id': user_id})


class SecuritySettingsView(PasswordChangeView, LoginRequiredMixin):
    model = CustomUser
    template_name = 'users/settings/security.html'
    form_class = ChangePasswordForm

    # def get_object(self):
    #     user_id = self.kwargs.get('user_id')
    #     return self.model.objects.get(pk=user_id)

    def get_success_url(self):
        user_id = self.kwargs.get('user_id')
        return reverse_lazy('profile-settings-security', kwargs={'user_id': user_id})
