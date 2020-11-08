from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('/', include('stud_app.urls')),
    # path('accounts/',include('stud_app.urls')),
    path('admin/', admin.site.urls),
    path('students/', include('stud_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)