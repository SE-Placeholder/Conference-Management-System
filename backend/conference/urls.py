from django.urls import path
from conference.views import ConferenceViewSet, JoinConferenceView, DesignateReviewersView

urlpatterns = [
    path('', ConferenceViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('/<int:id>', ConferenceViewSet.as_view({'get': 'retrieve', 'post': 'partial_update'})),
    path('/<int:id>/join', JoinConferenceView.as_view()),
    path('/<int:id>/designate-reviewers', DesignateReviewersView.as_view())
]