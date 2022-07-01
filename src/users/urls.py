from django.urls import path, reverse_lazy
from django.contrib.auth.views import *
from .views import *

urlpatterns = [
    path('profile/<slug:user_slug>/', ProfileView.as_view(), name='profile'),
    path('profile/settings/information/<int:user_id>/', InformationSettingsView.as_view(), name='profile-settings-information'),
    path('profile/settings/security/<int:user_id>/', SecuritySettingsView.as_view(), name='profile-settings-security'),
    path('profile/settings/site/<int:user_id>/', SiteSettingsView.as_view(), name='profile-settings-site'),
    path('profile/settings/notifications/<int:user_id>/', NotificationsSettingsView.as_view(), name='profile-settings-notifications'),
    # ajax
    path('validate-login-form/', login_validation_view, name='validate-login-form'),
    path('validate-registration-form/', registration_validation_view, name='validate-registration-form'),
    path('validate-email-form/', email_send_reset_view, name='validate-email-form'),
    path('get-user-comments/<slug:user_slug>/<int:num_comments>', get_user_comments_view, name='get-user-comments'),
    # password reset
    # path('reset-password/', PasswordResetView.as_view(template_name="password_reset_page.html"), name='reset_password'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_page.html', success_url=reverse_lazy('home')), name='password-reset-confirmation'),
]
