from django.db.models import Manager
from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework.fields import get_attribute

class PathPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def use_pk_only_optimization(self):
        return False

    def display_value(self, obj):
        names = obj.get_ancestors(include_self=True).values_list('name', flat=True)
        return ' / '.join(names[1:])

class DynamicQuerysetPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Allow callable queryset.
    """

    def __init__(self, *args, **kwargs):
        self.with_self = kwargs.pop('with_self', False)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        return self.eval_queryset(self.queryset)

    def eval_queryset(self, queryset):

        if callable(queryset):
            if self.with_self:
                return queryset(self)
            else:
                return queryset()

        if isinstance(queryset, (QuerySet, Manager)):
            return queryset.all()
        
        return queryset

class ChildQuerysetPrimaryKeyRelatedField(DynamicQuerysetPrimaryKeyRelatedField):
    """
    Get child queryset from other field.
    """

    def __init__(self, *args, **kwargs):
        assert 'parent_name' in kwargs, (
            '`parent_name` argument is not set.'
        )
        assert 'related_name' in kwargs, (
            '`related_name` argument is not set.'
        )
        self.parent_name = kwargs.pop('parent_name')
        self.related_name = kwargs.pop('related_name')
        queryset = kwargs.pop('queryset', self.get_child_queryset)
        super().__init__(queryset=queryset, *args, **kwargs)

    def get_child_queryset(self):
        instance = self.root.instance

        if instance:
            queryset = get_attribute(instance, (self.parent_name, self.related_name)) 
            return queryset.all()

class WriteQuerysetPrimaryKeyRelatedField(DynamicQuerysetPrimaryKeyRelatedField):
    """
    Set queryset on write and empty on read.
    """

    def __init__(self, *args, **kwargs):
        assert 'write_queryset' in kwargs, (
            '`write_queryset` argument is not set.'
        )
        self.write_queryset = kwargs.pop('write_queryset')
        super().__init__(queryset=self.get_write_queryset, *args, **kwargs)

    def get_write_queryset(self):

        if hasattr(self.root, 'initial_data'):
            return self.eval_queryset(self.write_queryset)

        return self.eval_queryset(self.write_queryset).none()