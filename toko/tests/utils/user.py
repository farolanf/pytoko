from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

PASSWORD = 'anypassword45'

def create_user():
    email = '%s@example.com' % get_random_string(16)
    username = get_random_string(16)
    password = get_random_string(16)
    user = User.objects.create(email=email, username=username, password=make_password(password))
    user.raw_password = password
    return user
