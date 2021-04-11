from django.urls import path

from paper.views import PaperViewSet

urlpatterns = [
    path('', PaperViewSet.as_view({'get': 'list', 'post': 'create'}), name='paper-list')
]

# path('/<int:id>', ConferenceViewSet.as_view({'get': 'retrieve'}), name='conference-detail'),