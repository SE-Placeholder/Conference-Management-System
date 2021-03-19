from django.urls import path
from .views import RegisterView, TokenObtainView, TokenRefreshView, TokenDisableView, PingView, RestrictedPingView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/get/', TokenObtainView.as_view(), name='get token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh token'),
    path('token/disable/', TokenDisableView.as_view(), name='disable token'),

    path('ping/', PingView.as_view(), name='ping'),
    path('rping/', RestrictedPingView.as_view(), name='restricted ping')
]
