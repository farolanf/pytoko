from django import forms
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import generic 
from django.views.generic.edit import FormView

from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticated

from toko import models
from toko.utils.validation import validate
from toko.utils.mail import send_mail
from toko.utils.password import create_password_reset, do_password_reset
from toko import forms

User = get_user_model()

class RegisterView(FormView):
    template_name = 'toko/account/register.html'
    form_class = forms.RegisterForm
    success_url = reverse_lazy('toko:register-success')

    def form_valid(self, form):
        username = 'user%s%s' % (get_random_string(3), User.objects.count())
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        User.objects.create_user(username=username, email=email, password=password)
        send_mail('Selamat datang', 'toko/mail/welcome.html', email)
        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'toko/account/login.html'
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse('toko:front'))

def logout_view(request):
    logout(request)
    return redirect('toko:front')

#=======================================

# class AnonView(views.APIView):
#     authentication_classes = ()
#     permission_classes = ()

# class PasswordEmailView(AnonView):
#     throttle_classes = (PasswordEmailThrottle,)

#     def post(self, request):
#         serializer = PasswordEmailRequestSerializer(data=request.data)
#         validate(serializer, 'Tidak dapat memproses reset password.')

#         email = serializer.validated_data['email']
#         token = create_password_reset(email)
#         url = '%sreset-password?t=%s' % (request.build_absolute_uri('/'), token)

#         send_mail('Password reset', 'toko/mail/password_reset.html', email, 
#                 context={'url': url})

#         return Response({
#             'message': 'Permintaan sedang diproses. Silahkan periksa email anda beberapa saat lagi.'
#         })

# class PasswordResetView(AnonView):

#     def post(self, request):
#         serializer = PasswordResetSerializer(data=request.data)
#         validate(serializer, 'Tidak dapat mereset password.')
#         do_password_reset(serializer.validated_data.get('token'),      
#                 serializer.validated_data.get('password'))
#         return Response({
#             'message': 'Password telah diubah. Silahkan masuk menggunakan password baru anda.'
#         })