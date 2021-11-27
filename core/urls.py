# -*- encoding: utf-8 -*-

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("university_connect.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
