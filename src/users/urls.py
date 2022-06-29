from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('validate-registration-form/', registration_validation_view, name='validate-registration-form'),
    path('validate-login-form/', login_validation_view, name='validate-login-form'),
    path('profile/settings/information/<int:user_id>/', InformationSettingsView.as_view(), name='profile-settings-information'),
    path('profile/settings/security/<int:user_id>/', SecuritySettingsView.as_view(), name='profile-settings-security'),
    path('profile/settings/site/<int:user_id>/', SiteSettingsView.as_view(), name='profile-settings-site'),
    path('profile/settings/notifications/<int:user_id>/', NotificationsSettingsView.as_view(), name='profile-settings-notifications'),
]
