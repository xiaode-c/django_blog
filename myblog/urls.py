"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django_blog import settings
from myblog.views import *


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/admin/ckeditor/', include('ckeditor_uploader.urls')),
    url(r"^uploads/(?P<path>.*)$", "django.views.static.serve", {"document_root": settings.MEDIA_ROOT, }),
    url(r'^$', article_view, name='index'),
    url(r'^article/(?P<title>\S+)$', content_detail, name='article_content'),
    url(r'^category/(?P<category>\S+)$', get_category, name='category'),
    url(r'^Tag/(?P<tag>\S+)$', get_tag, name='tag'),
    url(r'^search/$', search, name='search'),
    url(r'^archive/$', get_archive, name='archive'),
    url(r'^message/$', message, name='message'),
    url(r'^me/$', me, name='me'),
]
