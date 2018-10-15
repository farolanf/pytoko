from rest_framework.serializers import ValidationError

def validate_unique(model, field, message=None):
    def validate(value):
        nonlocal message
        if model.objects.filter(**{field: value}).exists():
            if not message:
                message = '%s sudah ada' % field.capitalize()
            raise ValidationError(message)
    return validate