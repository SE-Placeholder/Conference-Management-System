from django.urls import path

from submission.views import SubmissionViewSet

urlpatterns = [
    path('', SubmissionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('/<int:id>', SubmissionViewSet.as_view({'get': 'retrieve', 'post': 'partial_update'}))
]
