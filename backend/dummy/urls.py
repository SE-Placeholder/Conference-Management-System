from django.urls import path

from dummy.views import ConferenceListView, RestrictedConferenceListView

urlpatterns = [
    path('restricted/conferences/', RestrictedConferenceListView.as_view()),
    path('conferences/', ConferenceListView.as_view())
]