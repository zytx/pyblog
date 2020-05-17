from rest_framework import serializers

from pyblog import models
from .fields import SlugObjAttrRelatedField


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'
        extra_kwargs = {
            'uid': {'format': 'hex'}
        }


class PostSerializer(serializers.ModelSerializer):
    tags = SlugObjAttrRelatedField(many=True, slug_field='uid', attr_name='hex', queryset=models.Tag.objects.all())

    class Meta:
        model = models.Post
        fields = '__all__'
        extra_kwargs = {
            'uid': {'format': 'hex'},
            'created_time': {'format': '%s'},
            'updated_time': {'format': '%s'}
        }
