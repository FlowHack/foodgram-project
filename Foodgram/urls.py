from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

handler404 = 'Recipes.views.page_not_found'
handler500 = 'Recipes.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('Recipes.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS
    )
