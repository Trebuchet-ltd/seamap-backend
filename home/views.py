import numpy as np
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from constants import SCALES, LAT_RESOLUTION, LON_RESOLUTION
from .models import Image
from .serializers import ImageSerializer

# Create your views here.

depths = [
    0, 5, 10, 15, 20, 25, 30, 35, 40, 45,
    50, 55, 60, 65, 70, 75, 80, 85, 90, 95,
    100, 125, 150, 175, 200, 225, 250, 275, 300, 325,
    350, 375, 400, 425, 450, 475, 500, 550, 600, 650,
    700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150,
    1200, 1250, 1300, 1350, 1400, 1450, 1500
]


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
        try:
            graph_type = request.GET['graph_type']
            map_type = request.GET['type']
            time = round(float(request.GET['time']))
            lat, lon = [round(float(request.GET[a]) / SCALES[map_type]) for a in ["lat", "lon"]]
        except KeyError as er:
            return Response({"error": str(er)}, status=400)

        data_raw = np.load(f"data/{graph_type}/{time}.npy", mmap_mode="r")[:, lat, lon]
        data = []

        print(f"{0} {lat=} {lon=} {data_raw[0]=}")

        for i in range(len(data_raw)):
            if np.isnan(data_raw[i]):
                continue
            data.append({"y": depths[i], "x": data_raw[i]})

        return Response({"data": data}, status=status.HTTP_200_OK)


@api_view(('GET',))
def get_spot(request):
    layer = round(float(request.GET["layer"]))
    m_type = request.GET["type"]

    lat, lon = [round(float(request.GET[a]) / SCALES[m_type]) for a in ["lat", "lon"]]

    response = {}

    for map_type in ["s_an", "t_an"]:
        response[map_type] = []
        for time in range(12):
            d = np.load(f"data/{map_type}/{time}.npy", mmap_mode="r")
            print(f"{time} {lat=} {lon=} {d[time, lat, lon]=}")
            if not np.isnan(d[layer, lat, lon]):
                response[map_type].append(d[layer, lat, lon])

    response["bath"] = [round(-np.load("data/bath.npy", mmap_mode="r")[lat * SCALES["bath"], lon * SCALES["bath"]],
                              1)] * 12

    response["lat"] = lat * LAT_RESOLUTION - 90
    response["lon"] = lon * LON_RESOLUTION - 180

    return Response(response, status=status.HTTP_200_OK)


@api_view(('GET',))
def get_depths(request):
    return Response({"depths": depths}, status=status.HTTP_200_OK)
