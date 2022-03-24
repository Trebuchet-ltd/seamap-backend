from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
# Setup the URLs and include login URLs for the browsable API.
router = DefaultRouter()

urlpatterns = [
    path(r'', include(router.urls)),
]