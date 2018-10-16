from rest_framework.serializers import ValidationError

def validate_unique(model, field, message=None):
    def validate(value):
        nonlocal message
        if model.objects.filter(**{field: value}).exists():
            if not message:
                message = '%s sudah ada' % field.capitalize()
            raise ValidationError(message)
    return validate

def validate_exists(model, field, message=None):
    def validate(value):
        nonlocal message
        if not model.objects.filter(**{field: value}).exists():
            if not message:
                message = '%s tidak ditemukan' % field.capitalize()
            raise ValidationError(message)
    return validate