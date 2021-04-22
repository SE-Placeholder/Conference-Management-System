from django.urls import path

from role.views import UserConferencesView, UserSubmissionsView, UserListView

urlpatterns = [
    # lol
    path('s', UserListView.as_view()),
    path('/conferences', UserConferencesView.as_view()),
    path('/submissions', UserSubmissionsView.as_view())
]
