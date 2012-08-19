from models import ApiKey
from django.contrib import auth

class ApiKeyMiddleware(object):
    def process_request(self, request):
        if 'HTTP_APIKEY' not in request.META:
            return None

        auth_string = request.META['HTTP_APIKEY']

        if not auth_string:
            return None

        key = ApiKey.objects.get(key=auth_string)

        if not key:
            return None

        if key.user:
            request.user = key.user
        return
