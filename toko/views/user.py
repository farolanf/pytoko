from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import serializers

from toko.serializers import LoginSerializer
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

class RegisterView(FormView):
    pass

# class XRegisterView(FormView):
#     template_name = 'toko/account/register.html'
#     form_class = forms.RegisterForm
#     success_url = reverse_lazy('toko:register-success')

#     def form_valid(self, form):
#         username = 'user%s%s' % (get_random_string(3), User.objects.count())
#         email = form.cleaned_data.get('email')
#         password = form.cleaned_data.get('password')
#         User.objects.create_user(username=username, email=email, password=password)
#         send_mail('Selamat datang', 'toko/mail/welcome.html', email)
#         return super().form_valid(form)

# class XLoginView(FormView):
#     template_name = 'toko/account/login.html'
#     form_class = forms.LoginForm

#     def form_valid(self, form):
#         email = form.cleaned_data.get('email')
#         password = form.cleaned_data.get('password')
#         user = authenticate(username=email, password=password)
#         login(self.request, user)
#         return super().form_valid(form)

#     def get_success_url(self):
#         return self.request.GET.get('next', reverse('toko:front'))

def logout_view(request):
    logout(request)
    return redirect('toko:front')
