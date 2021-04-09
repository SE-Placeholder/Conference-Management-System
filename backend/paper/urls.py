from django.urls import path

from paper.views import ListPapersView

urlpatterns = [
    path('', ListPapersView.as_view())
]