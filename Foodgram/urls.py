from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages.views import flatpage
from django.urls import include, path

handler404 = 'Recipes.views.page_not_found'
handler500 = 'Recipes.views.server_error'

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('about-author/', flatpage, {'url': '/about-author/'}, name='about'),
    path('about-spec/', flatpage, {'url': '/about-spec/'}, name='terms'),
    path('api/', include('Api.urls')),
    path('', include('Users.urls', namespace='users')),
    path('', include('Recipes.urls', namespace='recipes'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS
    )
