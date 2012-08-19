# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required()
def api_status(request):
    x = ''
    if request.META.get('HTTP_APIKEY'):
        x = 'using APIKEY(%s)' % request.META.get('HTTP_APIKEY')
    return HttpResponse("Success: %s\n" % x)

