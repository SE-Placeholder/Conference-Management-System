from django.urls import path
from conference.views import ConferenceViewSet, JoinConferenceView

urlpatterns = [
    path('', ConferenceViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('/<int:id>', ConferenceViewSet.as_view({'get': 'retrieve', 'post': 'partial_update'})),
    path('/<int:id>/join', JoinConferenceView.as_view())
]