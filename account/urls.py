#coding=utf-8
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='UserViewSet')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/$', LoginView.as_view())
]
