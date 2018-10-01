from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

def create_user(email, password):
    return User.objects.create(email=email, password=make_password(password))
