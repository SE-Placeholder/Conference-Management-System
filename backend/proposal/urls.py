from django.urls import path

from proposal.views import ProposalViewSet

urlpatterns = [
    path('', ProposalViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('/<int:id>', ProposalViewSet.as_view({'get': 'retrieve', 'post': 'partial_update'}))
]
