from django.urls import path

from conference.views import ListConferencesView, GetConferenceView, AddConferenceView

# TODO: add name tags
urlpatterns = [
    path('list/', ListConferencesView.as_view()),
    path('get/<int:id>', GetConferenceView.as_view()),
    path('add/', AddConferenceView.as_view())
]