from django.http import Http404
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView, FormView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import *
from ..models import User, Profile


class InformationSettingsView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/settings/information.html'
    login_url = 'home'
    fields = ['avatar', 'username', 'email']

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return self.model.objects.get(pk=user_id)

    def get_success_url(self):
        user_id = self.kwargs.get('user_id')
        return reverse_lazy('profile-settings-information', kwargs={'user_id': user_id})


class SiteSettingsView(LoginRequiredMixin, UpdateView):
    model = Profile
    login_url = 'home'
    template_name = 'users/settings/site.html'
    fields = ['description', 'age']

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return self.model.objects.get(user__pk=user_id)

    def get_success_url(self):
        user_id = self.kwargs.get('user_id')
        return reverse_lazy('profile-settings-site',
                            kwargs={'user_id': user_id})

class NotificationsSettingsView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'users/settings/notifications.html'
    login_url = 'home'
    fields = (
        'notificate_planning',
        'notificate_reading',
        'notificate_read',
        'notificate_abandonded'
    )

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return self.model.objects.get(user__pk=user_id)

    def get_success_url(self):
        user_id = self.kwargs.get('user_id')
        return reverse_lazy('profile-settings-notifications',
                            kwargs={'user_id': user_id})


class SecuritySettingsView(LoginRequiredMixin, PasswordChangeView):
    model = User
    template_name = 'users/settings/security.html'
    login_url = 'home'
    form_class = ChangePasswordForm

    # def get_object(self):
    #     user_id = self.kwargs.get('user_id')
    #     return self.model.objects.get(pk=user_id)

    def get_success_url(self):
        user_id = self.kwargs.get('user_id')
        return reverse_lazy('profile-settings-security', kwargs={'user_id': user_id})
