from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from rest_framework import serializers

from toko.serializers import LoginSerializer, RegisterSerializer
from toko.utils.mail import send_mail
from toko.utils.password import create_password_reset, do_password_reset
from toko.forms import AnonFormView

User = get_user_model()

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
        send_mail('Selamat datang', 'toko/mail/welcome.html', data['email'])

def logout_view(request):
    logout(request)
    return redirect('toko:front')
