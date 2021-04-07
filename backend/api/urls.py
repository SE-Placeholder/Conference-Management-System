from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from dj_rest_auth.views import LogoutView, PasswordChangeView, UserDetailsView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/user/', UserDetailsView.as_view(), name='user_details'),
    path('auth/password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('auth/password/reset/', PasswordResetView.as_view(), name='password_reset'),
    # TODO: custom serializer for password reset confirm
    path('auth/password/reset/confirm/<slug:uidb64>/<slug:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # TODO: auth/token/verify/ TokenVerifyView.as_view() [name='token_verify']
    # TODO: auth/token/refresh/ get_refresh_view().as_view() [name='token_refresh']

    # path('', include('dummy.urls')),
    path('user/', include('role.urls')),
    path('conference/', include('conference.urls')),
    path('paper/', include('paper.urls'))
]
