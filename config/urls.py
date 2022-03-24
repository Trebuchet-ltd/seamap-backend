from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, authentication

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="description",

        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="sunithvs2002@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(authentication.SessionAuthentication,),

)
urlpatterns = [
                  path('', include('auth_login.urls')),
                  path('api/', include('home.urls')),
                  path('auth/', include('authentication.urls')),
                  path('openid/', include('oidc_provider.urls', namespace='oidc_provider')),
                  re_path(r'swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                          name='schema-json'),
                  path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
                  path(settings.ADMIN_URL + 'log_viewer/', include('log_viewer.urls')),
                  path(settings.ADMIN_URL, admin.site.urls),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
