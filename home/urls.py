from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Setup the URLs and include login URLs for the browsable API.
from .views import ImageViewSet

router = DefaultRouter()
router.register(ImageViewSet, 'image')
urlpatterns = [
    path(r'', include(router.urls)),
]
