from django.shortcuts import render
from rest_framework import views,viewsets,generics
from graduatethesis.models import *
from graduatethesis import serializers
# Create your views here.
class NguoiDungViewSet(viewsets.ViewSet,generics.ListAPIView):
    queryset = NguoiDung.objects.all()
    serializer_class =  serializers.NguoiDungSerializer
