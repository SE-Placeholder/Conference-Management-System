from django.urls import path

from proposal.views import ProposalViewSet, BidProposalView

urlpatterns = [
    path('', ProposalViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('/<int:id>', ProposalViewSet.as_view({'get': 'retrieve', 'post': 'partial_update'})),
    path('/<int:id>/bid', BidProposalView.as_view({'post': 'create', 'get': 'retrieve', 'put': 'partial_update'}))
]
