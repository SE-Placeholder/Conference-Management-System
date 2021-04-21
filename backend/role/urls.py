from django.urls import path

from role.views import UserConferencesView, UserPapersView, UserListView

urlpatterns = [
    # lol
    path('s', UserListView.as_view()),
    path('/conferences', UserConferencesView.as_view()),
    path('/papers', UserPapersView.as_view())
]
