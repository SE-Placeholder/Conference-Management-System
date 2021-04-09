from django.urls import path

from dummy.views import ConferenceListView, RestrictedConferenceListView

urlpatterns = [
    path('conferences', RestrictedConferenceListView.as_view()),
    path('non-restricted/conferences', ConferenceListView.as_view())
]