from models import ApiKey
from django.contrib import auth


class ApiKeyMiddleware(object):
    def process_request(self, request):
        auth_string = request.META.get('HTTP_APIKEY')

        if not auth_string:
            return None

        key = ApiKey.objects.get(key=auth_string)

        if not key:
            return None

        if key.user:
            key.login(request.META.get('REMOTE_ADDR'))
            request.user = key.user
        return
