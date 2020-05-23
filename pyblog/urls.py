from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path(r'', views.Index.as_view(), name='index'),
    path(r'admin/', admin.site.urls),
    path(r'archive/', views.ArchiveView.as_view(), name='archive'),
    path(r'tag/<title>/', views.TagListView.as_view(), name='tag'),
    path(r'auth/', include('authentication.urls')),

    path(r'api/', include('api.urls', namespace='api')),

    path(r'<slug:slug>/', views.PostDetailView.as_view(), name='post')
]
