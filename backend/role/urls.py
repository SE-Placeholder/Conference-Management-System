from django.urls import path

from role.views import UserViewSet

urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('/<str:username>', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail')
]
