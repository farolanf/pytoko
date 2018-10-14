from django.conf import settings

def method_unwrap(get_response):

    def middleware(request):

        method = request.POST.get('_method', None)

        if method and request.method == 'POST':
            request.method = method.upper()
            request.META['REQUEST_METHOD'] = request.method
            
            csrf_token = request.POST.get('csrfmiddlewaretoken', None)
            if csrf_token:
                request.META[settings.CSRF_HEADER_NAME] = csrf_token

        return get_response(request)

    return middleware