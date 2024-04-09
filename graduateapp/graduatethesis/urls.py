from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from graduatethesis import views
r = routers.DefaultRouter()
urlpatterns = [
    path('', include(r.urls))
]