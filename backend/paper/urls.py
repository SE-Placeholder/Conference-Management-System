from django.urls import path

from paper.views import PaperViewSet

urlpatterns = [
    path('', PaperViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('/<int:id>', PaperViewSet.as_view({'get': 'retrieve', 'post': 'partial_update'}))
]
