from django.shortcuts import render
from rest_framework.generics import ListAPIView

from paper.models import Paper
from paper.serializers import PaperSerializer


class ListPapersView(ListAPIView):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer

