"""selstagram_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework_nested import routers as drf_nested_routers
from rest_framework import routers as drf_routers

from selsta101 import views as selsta101_views

router = drf_nested_routers.DefaultRouter()
router.register('tags', selsta101_views.TagViewSet)

tags_router = drf_nested_routers.NestedSimpleRouter(router, 'tags', lookup='tag')
tags_router.register('media', selsta101_views.InstagramMediaViewSet, base_name='media')

urlpatterns = [
    url(r'^verify_receipt', selsta101_views.verify_receipt),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^', include(tags_router.urls)),
]
