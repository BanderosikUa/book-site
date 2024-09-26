from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import PasswordResetConfirmView
from .views import (
    ProfileView, InformationSettingsView, SecuritySettingsView,
    SiteSettingsView, NotificationsSettingsView, login_validation_view,
    registration_validation_view, email_send_reset_view
)
from .apis import UserCommentListApi


urlpatterns = [
    path(
        "profile/",
        include([
            path('<slug:user_slug>/', ProfileView.as_view(), name='profile'),
            path('<int:user_id>/settings/information/', InformationSettingsView.as_view(), name='profile-settings-information'),
            path('<int:user_id>/settings/security/', SecuritySettingsView.as_view(), name='profile-settings-security'),
            path('<int:user_id>/settings/site/', SiteSettingsView.as_view(), name='profile-settings-site'),
            path('<int:user_id>/settings/notifications/', NotificationsSettingsView.as_view(), name='profile-settings-notifications'),
        ])
    ),
    path(
        "auth/",
        include([
            path('login/', login_validation_view, name='login'),
            path('register/', registration_validation_view, name='register'),
            path('validate/email/', email_send_reset_view, name='validate-email'),
            path('password/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_page.html', success_url=reverse_lazy('home')), name='password-reset-confirmation'),
        ])
    ),
    path('users/<int:user_id>/comments/', UserCommentListApi.as_view(), name='get-user-comments'),
]
