from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import get_template
from django.contrib.auth import get_user_model, authenticate
from . import models

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

class AttrsMixin(object):
    attrs = {}

    def __init__(self, attrs={}):
        final_attrs = dict(list(attrs.items()) + list(self.attrs.items()))
        super().__init__(attrs=final_attrs)

class InputMixin(AttrsMixin):
    attrs = {
        'class': 'input'
    }

# Widgets ####################################################################

class TextInput(forms.TextInput):
    template_name = 'toko/widgets/input.html'

class Textarea(AttrsMixin, forms.Textarea):
    attrs = {
        'class': 'textarea'
    }

class EmailInput(InputMixin, forms.EmailInput):
    pass

class PasswordInput(InputMixin, forms.PasswordInput):
    pass

class Select(forms.Select):
    template_name = 'toko/widgets/select.html'

# Fields #####################################################################

class CharField(forms.CharField):
    widget = TextInput

class EmailField(forms.EmailField):
    widget = EmailInput

class PasswordField(forms.CharField):
    widget = PasswordInput

class TreeChoiceField(forms.ModelChoiceField):
    widget = Select

    def label_from_instance(self, obj):
        ancestors = obj.get_ancestors(include_self=True).values_list('name', flat=True)
        return ' / '.join(ancestors[1:]) 

# Validators #################################################################

email_unique = validate_unique(User, 'email', message='Email sudah terdaftar')

# Forms ######################################################################

class FormOutputMixin:

    def __str__(self):
        output = []
        
        field_template = get_template('toko/form/field.html')

        for field in self:
            output.append(field_template.render({'field': field}))

        return mark_safe('\n'.join(output))

class ModelFormBase(FormOutputMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'init') and callable(self.init):
            self.init()

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

class AdModelFormBase(ModelFormBase):
    category = TreeChoiceField(
        models.Taxonomy.objects.get(slug='kategori').get_descendants(),
    )
    title = CharField(min_length=10, max_length=70)
    desc = CharField(min_length=20, max_length=4000, widget=Textarea, help_text='Terangkan produk/jasa dengan singkat dan jelas, beserta kekurangannya jika ada.')

    def init(self):
        provinsi = models.Provinsi.objects.get(pk=self['provinsi'].value())
        self['kabupaten'].queryset = provinsi.kabupaten_set.all()

AdForm = forms.modelform_factory(
    models.Ad,
    form=AdModelFormBase,
    fields=('category', 'title', 'desc', 'price', 'nego', 'provinsi', 'kabupaten'),
    widgets={
        'price': TextInput,
        'provinsi': Select,
        'kabupaten': Select,
    },    
)