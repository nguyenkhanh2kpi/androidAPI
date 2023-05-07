from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import filters
from .models import *
from .serializer import *

class DivineCategoryList(ListAPIView):
    queryset = DivineCategory.objects.all()
    serializer_class = DivineCategorySerializer

class DivineSoftwareList(ListAPIView):
    queryset = DivineSoftware.objects.all()
    serializer_class = DivineSoftwareSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category__name']

class DivineSoftwareDetail(RetrieveAPIView):
    queryset = DivineSoftware.objects.all()
    serializer_class = DivineSoftwareSerializer

class DivineKeyList(ListAPIView):
    queryset = DivineKey.objects.all()
    serializer_class = DivineKeySerializer

class DivineCommentList(ListAPIView):
    queryset = DivineComment.objects.all()
    serializer_class = DivineCommentSerializer

