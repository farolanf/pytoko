
class FilterFieldsMixin(object):
    """
    Allow filtering fields based on permissions. 
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.view = kwargs.pop('view', None)
        super().__init__(*args, **kwargs)

    def get_field_names(self, *args, **kwargs):
        fields = super().get_field_names(*args, **kwargs)

        if self.instance is not None and \
            self.request is not None and self.view is not None:

            # filter based on permissions
            if hasattr(self, 'Meta') and hasattr(self.Meta, 'field_permissions'):
                fields = self.apply_field_permissions(fields)

            # call filter method if defined
            if hasattr(self, 'filter_fields'):
                fields = self.filter_fields(fields)

        return fields

    def apply_field_permissions(self, fields):
        return [field for field in fields if self.field_allowed(field)]

    def field_allowed(self, field):
        for perm in self.Meta.field_permissions:
            if not field in perm['fields']: continue
            permissions = [permission() for permission in perm['permission_classes']]
            for permission in permissions:
                if not permission.has_object_permission(self.request, self.view, self.instance):
                    return False
        return True