from django.shortcuts import render
import django_filters
from django.db.models import Q
from django.http import HttpResponseRedirect
from rest_framework import permissions
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Image
from .serializers import ImageSerializer
from .utils import get_plot


# Create your views here.


class ImageViewSet(viewsets.ModelViewSet):
    """
    API end point to get all product details
    """
    http_method_names = ['get']
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get", ], url_path='plot')
    def plot(self, request, *args, **kwargs):
        time = request.data['time']
        lat = request.data['lat']
        long = request.data['long']
        svg_str = get_plot(lat, long, time)
        return Response({"svg": svg_str}, status=status.HTTP_200_OK)
