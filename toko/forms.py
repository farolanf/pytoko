from collections import defaultdict
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST

class FormView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = None
    template = None
    success_url = '/'

    # validate params on GET request using serializer if True,
    # else use check_params()
    validate_params = False
    params_serializer_class = None
    
    failed_params_template = ''

    def get(self, request, **kwargs):

        try:
            if self.validate_params:
                self.do_validate_params(**kwargs)
            else:
                self.check_params(**kwargs)
        except serializers.ValidationError as exc:
            return self.get_failed_params_response(errors=exc.detail, exc=exc, **kwargs)
        
        # assign kwargs to data and provide empty str for missing fields
        data = defaultdict(str)
        data.update(kwargs)

        serializer = self.serializer_class(data)

        return Response({
            'serializer': serializer,
        }, template_name=self.template)

    def post(self, request):
        errors = None

        self.serializer = self.serializer_class(data=request.data)

        if self.serializer.is_valid():
            try:
                self.form_valid(self.serializer.data)
                return redirect(self.success_url)
            except serializers.ValidationError as exc:
                errors = exc.detail

        return Response({
            'errors': errors,
            'serializer': self.serializer
        }, template_name=self.template, status=HTTP_400_BAD_REQUEST)

    def fail(self, msg, code=None):
        raise serializers.ValidationError(msg, code)

    def do_validate_params(self, **kwargs):
        assert self.params_serializer_class, (
            '`params_serializer_class` is not set.'
        )
        data = dict()
        data.update(kwargs)
        serializer = self.params_serializer_class(data=data)
        if not serializer.is_valid():
            raise serializers.ValidationError(serializer.errors)

    def check_params(self, **kwargs):
        pass 

    def get_failed_params_response(self, errors=None, exc=None, **kwargs):
        return Response({
            'errors': errors,
            'params': kwargs,
        }, template_name=self.failed_params_template, status=HTTP_400_BAD_REQUEST)

    def form_valid(self, data):
        pass

class AnonFormView(FormView):
    authentication_classes = ()
    permission_classes = ()
