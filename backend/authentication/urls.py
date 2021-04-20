from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from dj_rest_auth.views import LogoutView, PasswordChangeView
from django.urls import path

from authentication.views import IsAuthenticatedView

urlpatterns = [
    path('/login', LoginView.as_view(), name='login'),
    path('/logout', LogoutView.as_view(), name='logout'),
    path('/register', RegisterView.as_view(), name='register'),
    path('/is-authenticated', IsAuthenticatedView.as_view(), name='is_authenticated'),
    path('/password/change', PasswordChangeView.as_view(), name='password_change'),
    path('/password/reset', PasswordResetView.as_view(), name='password_reset'),
    # TODO: custom serializer for password reset confirm
    path('/password/reset/confirm/<slug:uidb64>/<slug:token>', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm')
]
