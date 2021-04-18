from django.urls import path

from role.views import UserConferencesView

urlpatterns = [
    # path('', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    # path('/<str:username>', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail')
    path('/conferences', UserConferencesView.as_view())
]
