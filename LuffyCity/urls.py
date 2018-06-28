"""LuffyCity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from Luffy import views
from django.views.static import serve
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^index/$", views.index),
    re_path(r"^index/(?P<team>\d+)/$", views.index),
    re_path(r"^login/$", views.login),
    re_path(r"^detail/$", views.detail),
    re_path(r"^edit/$", views.editinfo),
    re_path(r"^editmoteam/$", views.editmoteam),
    re_path(r"^$", views.login),
    re_path(r"^logout/$", views.logout),
    re_path(r"^register/$", views.register),
    re_path(r"^getdata/$", views.getdata),
    re_path(r"^get_code/$", views.get_code),
    re_path(r"^summary/$", views.summary),
    re_path(r'^media/(?P<path>.*)/$', serve, {"document_root": settings.MEDIA_ROOT}),

]
