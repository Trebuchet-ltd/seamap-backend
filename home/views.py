from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Image
from .serializers import ImageSerializer
from .plotter import get_plot

# Create your views here.


class ImageViewSet(viewsets.ModelViewSet):
    """
    API end point to get all product details
    """
    http_method_names = ['get']
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get", ], url_path='plot')
    def plot(self, request, *args, **kwargs):

        print(request.GET)
        try:
            map_type = request.GET['type']
            time = request.GET['time']
            lat = request.GET['lat']
            long = request.GET['lon']
        except KeyError as er:
            print(er)
            return Response({"error": str(er)}, status=400)

        try:
            data = get_plot(map_type, lat, long, time)
        except Exception as er:
            print(er)
            return Response({"error": str(er)}, status=400)

        return Response({"data": data}, status=status.HTTP_200_OK)
