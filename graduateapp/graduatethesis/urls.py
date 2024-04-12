from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from graduatethesis import views
r = routers.DefaultRouter()
r.register('nguoidung',views.NguoiDungViewSet,basename="nguoidung")
urlpatterns = [
    path('', include(r.urls))
]