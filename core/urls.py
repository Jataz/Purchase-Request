from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('myapp.urls')),  # Adjusted to avoid conflict
    path('', RedirectView.as_view(url='/login/', permanent=True)),  # Root URL redirect
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
