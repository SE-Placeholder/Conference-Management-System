from django.urls import path

from conference.views import ConferenceViewSet

urlpatterns = [
    path('', ConferenceViewSet.as_view({'get': 'list', 'post': 'create'}), name='conference-list'),
    # TODO: update and delete
    path('/<int:id>', ConferenceViewSet.as_view({'get': 'retrieve'}), name='conference-detail'),
]