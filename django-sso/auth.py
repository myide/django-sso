import requests
try:
    from collections import UserDict
except ImportError:
    from UserDict import UserDict
from rest_framework import status

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin

UserModel = get_user_model()

class User(UserDict):

    def __init__(self, data):
        self.data = data

    @property
    def email(self):
        return self.data.get("email")

    @property
    def is_active(self):
        return self.data.get("is_active")

    @property
    def username(self):
        return self.data.get("username")

    @property
    def cname(self):
        return self.data.get("cname")

    @property
    def departments(self):
        return self.data.get("departments")

class HandleUser:

    def get_or_create_user(user):
        kwargs = {
            'email': user.email,
            'username': user.username
        }
        try:
            instance = UserModel.objects.get(username=user.username)
            instance.username = user.username
            instance.save()
            user = instance
        except UserModel.DoesNotExist:
            user, created = UserModel.objects.get_or_create(**kwargs)
        return user

class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        data = request.META.get('HTTP_AUTHORIZATION')
        if not data:
            return JsonResponse(data={
                "msg": 'Not Provide Authorization',
                'status': status.HTTP_401_UNAUTHORIZED,
                'data': {'detail': 'Not Provide Authorization'}},
                status=status.HTTP_401_UNAUTHORIZED)
        auth = RequestAuth(data)
        if not auth.query():
            return JsonResponse(data=auth.response, status=status.HTTP_403_FORBIDDEN)
        request.user = HandleUser.get_or_create_user(auth.user)

class RequestAuth:

    sso_url = settings.SSO_URL

    def __init__(self, data):
        self.data = data
        self._response = None

    def _request(self):
        try:
            response = requests.post(self.sso_url, headers=self.header)
            return self._validate(response)
        except Exception as err:
            self.error_response(err)
            return False

    def _validate(self, response):
        self._response = response.json()
        if response.status_code > 200:
            self.error_response("response status > 200")
            return False
        return self._response.get('is_active')

    def query(self):
        return self._request()

    def error_response(self, err):
        self._response = {
            'status': status.HTTP_401_UNAUTHORIZED,
            'msg': 'Auth user token error:{}'.format(err),
            'data': {}
        }

    @property
    def header(self):
        return {'Authorization': self.data}

    @property
    def response(self):
        return self._response

    @property
    def user(self):
        return User(self._response)
