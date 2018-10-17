from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from toko.models import PasswordReset

def create_password_reset(email):
    token = make_password(None)
    date = timezone.now()
    
    try:
        obj = PasswordReset.objects.get(email=email)
    except PasswordReset.DoesNotExist:
        PasswordReset.objects.create(email=email, token=token, created_at=date)
    else:
        obj.token = token
        obj.created_at = date
        obj.save()

    return token

def do_password_reset(token, password):
    password_reset = PasswordReset.objects.get(token=token)
    
    user = get_user_model().objects.get(email=password_reset.email)
    user.password = make_password(password)
    user.save()
    
    password_reset.delete()

    return password_reset
