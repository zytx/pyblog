from django.urls import path

from . import views

urlpatterns  = [
    path(r'posts', views.PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='posts'),
    path(r'posts/<uid>', views.PostViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'}), name='post-detail'),
    path(r'tags', views.TagViewSet.as_view({'get': 'list', 'post': 'create'}), name='tags'),
    path(r'tags/<uid>', views.TagViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'}), name='tag-detail'),
]

app_name = 'api'
