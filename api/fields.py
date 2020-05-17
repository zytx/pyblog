from rest_framework import serializers


class SlugObjAttrRelatedField(serializers.SlugRelatedField):

    def __init__(self, attr_name=None, **kwargs):
        assert attr_name is not None, 'The `attr_name` argument is required.'
        self.attr_name = attr_name
        super().__init__(**kwargs)

    def to_representation(self, obj):
        return getattr(super().to_representation(obj), self.attr_name)
