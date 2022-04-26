from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

import xarray as xr

from .models import Image
from .serializers import ImageSerializer
from .plotter import get_plot

# Create your views here.

# data_raw = xr.open_dataset("netcdf/woa_salt.nc", decode_times=False)


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

        print(request.GET)
        try:
            type = request.GET['type']
            time = request.GET['time']
            lat = request.GET['lat']
            long = request.GET['lon']
        except KeyError as er:
            print(er)
            return Response({"error": str(er)}, status=400)

        try:
            # svg_str = get_plot(data_raw, type, lat, long, time)
            svg_str = "No DATA FILE !!!"
        except Exception as er:
            print(er)
            return Response({"error": str(er)}, status=400)

        return Response({"svg": svg_str}, status=status.HTTP_200_OK)
