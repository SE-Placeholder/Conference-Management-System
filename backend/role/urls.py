from django.urls import path

from role.views import UserConferencesView, UserProposalsView, UserListView

urlpatterns = [
    # lol
    path('s', UserListView.as_view()),
    path('/conferences', UserConferencesView.as_view()),
    path('/proposals', UserProposalsView.as_view())
]
