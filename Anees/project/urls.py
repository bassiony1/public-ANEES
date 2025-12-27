from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import render


def render_react(request):
    return render(request, "index.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("core.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("api/", include("anees.urls")),
    re_path(r"^$", render_react),
    re_path(r"^(?:.*)/?$", render_react),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
