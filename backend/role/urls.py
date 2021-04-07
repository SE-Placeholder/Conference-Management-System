from django.urls import path

from role.views import ListUsersView, GetUserView

# TODO: name tags
urlpatterns = [
    path('list/', ListUsersView.as_view()),
    path('get/<str:username>/', GetUserView.as_view())
]
