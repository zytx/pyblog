from rest_framework import viewsets
from pyblog.models import Post, Tag
from . import serializers


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    lookup_field = 'uid'


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    lookup_field = 'uid'
