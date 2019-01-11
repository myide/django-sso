# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from utils.unitaryauth import UnitaryAuth
from .serializers import UserSerializer
from .models import User

# Create your views here.

class UserViewSet(ModelViewSet):
    '''
        用户信息
    '''
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    search_fields = ['username']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user)
        return Response(serializer.data)

class LoginView(UnitaryAuth, APIView):
    '''
        接入统一认证 backend
    '''
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        if not self.authenticate:
            raise AuthenticationFailed
        user_query = self.serializer_class.Meta.model.objects.filter(username=request.data.get('username'))
        if user_query:
            serializer = self.serializer_class(user_query[0], data=request.data)
        else:
            serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
