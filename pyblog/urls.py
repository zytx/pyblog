"""pyblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views

from django.views.static import serve
from . import settings

urlpatterns = [
    url(r'^$', views.Index.as_view(),name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^archive/$',views.Archive.as_view(),name='archive'),

    url(r'^media/(?P<path>.*)/$', serve, {'document_root':settings.MEDIA_ROOT}),
    
    url(r'^tag/(?P<slug>[0-9a-z-]+)/$',views.TagList.as_view(),name='tag'),
    url(r'^category/(?P<slug>[0-9a-z-]+)/$',views.CategoryList.as_view(),name='category'),
    
    url(r'^editormd/',include('editormd.urls')),
    url(r'^auth/',include('authentication.urls')),
    
    url(r'^(?P<slug>[0-9a-z-]+)/$',views.ArticleDetail.as_view(),name='article'),

]
