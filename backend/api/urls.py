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

from django.contrib import admin
from django.urls import path, include

# from dj_rest_auth import urls
# urls.LogoutView
# urls.LoginView
# urls.PasswordChangeView
# urls.PasswordResetConfirmView
# urls.PasswordResetView
# urls.TokenVerifyView
# urls.UserDetailsView

# from dj_rest_auth.registration import urls
# urls.RegisterView
# urls.VerifyEmailView
# urls.TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('', include('dummy.urls'))
]
