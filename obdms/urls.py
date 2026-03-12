from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("accounts/", include("accounts.urls")),
    path("donors/", include(("donors.urls", "donors"), namespace="donors")),
    path("hospital/", include(("hospitals.urls", "hospital"), namespace="hospital")),
    path("requests/", include(("blood_requests.urls", "requests"), namespace="requests")),
]

# Serve static and media files in development and production
if settings.DEBUG:
    # Development: Django serves static/media files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Production: WhiteNoise serves static files, but media still needs serving
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
