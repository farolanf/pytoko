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

    def get(self, request, **kwargs):
        serializer = self.serializer_class()

        return Response({
            'serializer': serializer,
            'params': kwargs,
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

    def form_valid(self, data):
        pass

class AnonFormView(FormView):
    authentication_classes = ()
    permission_classes = ()
