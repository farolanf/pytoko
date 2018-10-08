from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

def validate(serializer, message=''):
    """
    Validate a serializer and return error response on failure.
    This is to maintain consistent response structure.
    """
    if not serializer.is_valid():
        non_field_errors = serializer.errors.get('non_field_errors', [])
        non_field_errors.append(message)
        raise ValidationError({
            **serializer.errors,
            'non_field_errors': non_field_errors,
        })
    return True
