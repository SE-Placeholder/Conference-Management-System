from django.conf.urls import url

from conference.views import ping

urlpatterns = [
    url('ping', ping)
]