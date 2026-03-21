from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.products.urls')),
    path('api/', include('apps.bom.urls')),
    path('api/', include('apps.settings_app.urls')),
    path('api/', include('apps.eco.urls')),
    path('api/', include('apps.approvals.urls')),
    path('api/', include('apps.reports.urls')),
    path('api/', include('apps.audit.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
