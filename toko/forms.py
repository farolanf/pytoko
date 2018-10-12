from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

def validate_exists(model, field, message=None):
    def validate(value):
        nonlocal message
        if not model.objects.filter(**{field: value}).exists():
            if not message:
                message = '%s tidak ditemukan' % field.capitalize()
            raise forms.ValidationError(message)
    return validate

def validate_unique(model, field, message=None):
    def validate(value):
        nonlocal message
        if model.objects.filter(**{field: value}).exists():
            if not message:
                message = '%s sudah ada' % field.capitalize()
            raise forms.ValidationError(message)
    return validate

class InputMixin(object):

    def __init__(self, attrs={}):
        if hasattr(attrs, 'class'):
            attrs['class'] += ' input'
        else:
            attrs['class'] = 'input'
        super().__init__(attrs)

class TextInput(InputMixin, forms.TextInput):
    pass

class EmailInput(InputMixin, forms.EmailInput):
    pass

class PasswordInput(InputMixin, forms.PasswordInput):
    pass

class EmailField(forms.EmailField):
    widget = EmailInput

class CharField(forms.CharField):
    widget = TextInput

class PasswordField(forms.CharField):
    widget = PasswordInput

email_unique = validate_unique(User, 'email', message='Email sudah terdaftar')

class LoginForm(forms.Form):
    email = EmailField(max_length=100)
    password = PasswordField(max_length=32)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if not user:
            raise forms.ValidationError('Email atau password tidak terdaftar')
        return cleaned_data

class RegisterForm(forms.Form):
    email = EmailField(max_length=100, validators=[email_unique])
    password = PasswordField(min_length=8, max_length=32)
    password_confirm = PasswordField(label='Ulang password', min_length=8, max_length=32)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            self.add_error('password_confirm', 'Password tidak sama')
        return cleaned_data
