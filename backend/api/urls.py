"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.serializers import PasswordResetSerializer
from dj_rest_auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.contrib import admin
from django.urls import path, include

# from dj_rest_auth import urls
# urls.PasswordChangeView
# urls.PasswordResetConfirmView
# urls.
# urls.TokenVerifyView
# urls.UserDetailsView

# from dj_rest_auth.registration import urls
# urls.RegisterView
# urls.VerifyEmailView
# urls.TemplateView


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/register/', RegisterView.as_view(), name='register'),

    path('auth/password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('auth/password/reset/confirm/<slug:uidb64>/<slug:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # path('auth/', include('dj_rest_auth.urls')),
    # path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('', include('dummy.urls')),
    path('', include('roles.urls'))
]
