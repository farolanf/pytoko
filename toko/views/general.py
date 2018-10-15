from django.shortcuts import render
from django.core import exceptions
from rest_framework.views import exception_handler as _exception_handler
from rest_framework.exceptions import Throttled

def index(request):
    return render(request, 'toko/index.html')

def exception_handler(exc, context):
    request = context['request']

    response = _exception_handler(exc, context)

    if request.path.startswith('/api/'):
        return response

    if isinstance(exc, Throttled):
        return render(request, 'toko/throttled.html')

    if not response:
        return
    
    if response.status_code == 401:
        return render(request, 'toko/401.html')
    elif response.status_code == 403 or isinstance(exc, exceptions.PermissionDenied):
        return render(request, 'toko/403.html')
    elif response.status_code == 404:
        return render(request, 'toko/404.html')