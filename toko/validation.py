from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

def validate(serializer, message=''):
    """
    Validate a serializer and return error response on failure.
    This is to maintain consistent response structure.
    """
    if not serializer.is_valid():
        raise ValidationError({
            'message': message,
            'errors': serializer.errors
        })
    return True
