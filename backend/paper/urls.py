from django.urls import path

from paper.views import ListPapersView

urlpatterns = [
    path('list/', ListPapersView.as_view())
]