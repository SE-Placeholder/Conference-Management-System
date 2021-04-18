from django.urls import path

from paper.views import PaperViewSet

# TODO: list by conference?
urlpatterns = [
    path('', PaperViewSet.as_view({'get': 'list', 'post': 'create'}), name='paper-list')
]