import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

class UnitaryAuth(object):

    def check_sso(self, param):
        '''
            调sso认证后端，把用户和密码数据param作为参数; 返回True或False
            :param param:
            :return: True/False
        '''
        return True

    def check_auth(self, param):
        url = settings.AUTH_URL
        res = requests.post(url, json=param)
        if not res.ok:
            raise AuthenticationFailed(res.content)
        return res.json()

    @property
    def authenticate(self):
        data = self.request.data
        param = {
            'username':data.get('username'),
            'password':data.get('password')
        }
        if not self.check_sso(param):
            raise AuthenticationFailed
        return self.check_auth(param)
