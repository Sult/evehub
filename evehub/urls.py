from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^$', 'evetool.views.home', name='home'),
    url(r'^', include('users.urls')),
    url(r'^', include('admins.urls')),
    url(r'^', include('apis.urls')),
    url(r'^', include('characters.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
