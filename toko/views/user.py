from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import serializers

from toko.serializers import LoginSerializer, RegisterSerializer
from toko.utils.mail import send_mail
from toko.utils.password import create_password_reset, do_password_reset

User = get_user_model()

class FormView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = None
    template = None
    success_url = '/'

    def get(self, request):
        serializer = self.serializer_class()

        return Response({
            'serializer': serializer
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
        }, template_name=self.template)

    def fail(self, msg, code=None):
        raise serializers.ValidationError(msg, code)

    def form_valid(self, data):
        pass

class AnonFormView(FormView):
    authentication_classes = ()
    permission_classes = ()

class LoginView(AnonFormView):
    serializer_class = LoginSerializer
    template = 'toko/account/login.html'
    success_url = 'toko:front'

    def form_valid(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            self.fail('Email/password tidak terdaftar')
        login(self.request, user)

class RegisterView(AnonFormView):
    serializer_class = RegisterSerializer
    template = 'toko/account/register.html'
    success_url = 'toko:register-success'

    def form_valid(self, data):
        username = 'user%s%s' % (get_random_string(3), User.objects.count())
        User.objects.create_user(username=username, email=data['email'], password=data['password'])
        send_mail('Selamat datang', 'toko/mail/welcome.html', email)

def logout_view(request):
    logout(request)
    return redirect('toko:front')
