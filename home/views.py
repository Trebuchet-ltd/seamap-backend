import numpy as np
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from constants import SCALES, LAT_RESOLUTION, LON_RESOLUTION
from install import depths
from .models import Image
from .serializers import ImageSerializer

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
        try:
            graph_type = request.GET['graph_type']
            map_type = request.GET['type']
            time = round(float(request.GET['time']))
            lat, lon = [round(float(request.GET[a]) / SCALES[map_type]) for a in ["lat", "lon"]]
        except KeyError as er:
            return Response({"error": str(er)}, status=400)

        data_raw = np.load(f"data/{graph_type}/{time}.npy")[:, lat, lon]
        data = []

        print(f"{0} {lat=} {lon=} {data_raw[0]=}")

        for i in range(len(data_raw)):
            if np.isnan(data_raw[i]) or data_raw[i] == -2147483648:
                continue
            data.append({"y": depths[i], "x": data_raw[i]})

        return Response({"data": data}, status=status.HTTP_200_OK)


@api_view(('GET',))
def get_spot(request):
    layer = round(float(request.GET["layer"]))
    m_type = request.GET["type"]

    lat, lon = [round(float(request.GET[a]) / SCALES[m_type]) for a in ["lat", "lon"]]

    response = {}

    for map_type in ["s_an", "t_an", "s_nd", "c_an"]:
        response[map_type] = []
        for time in range(12):
            d = np.load(f"data/{map_type}/{time}.npy", mmap_mode="r")
            if not np.isnan(d[layer, lat, lon]) and d[layer, lat, lon] != -2147483648:
                response[map_type].append(d[layer, lat, lon])

    response["bath"] = [round(-np.load("data/bath.npy", mmap_mode="r")[lat * SCALES["bath"], lon * SCALES["bath"]],
                              1)] * 12

    response["lat"] = lat * LAT_RESOLUTION
    response["lon"] = lon * LON_RESOLUTION

    return Response(response, status=status.HTTP_200_OK)


@api_view(('GET',))
def get_depths(request):
    return Response({"depths": depths}, status=status.HTTP_200_OK)
