"""Test's urls view for django-filer-optimizer"""

from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path, re_path
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^filer/", include("filer.urls")),
]

urlpatterns += i18n_patterns(
    re_path(r"^jsi18n/$", JavaScriptCatalog.as_view(), name="javascript-catalog"),
)
