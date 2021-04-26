from django.urls import path

from proposal.views import ProposalViewSet, BidProposalView, AssignReviewersView

urlpatterns = [
    path('', ProposalViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('/<int:id>', ProposalViewSet.as_view({'get': 'retrieve', 'post': 'partial_update'})),
    path('/<int:id>/bid', BidProposalView.as_view()),
    path('/<int:id>/assign-reviewers', AssignReviewersView.as_view())
]
