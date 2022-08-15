
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('dj_rest_auth.urls')),
    path('api/account/registration/', include('dj_rest_auth.registration.urls')),
    path('api/store/', include('store.urls')),
]


urlpatterns += [
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
