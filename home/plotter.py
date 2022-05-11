import numpy as np

from install import SCALE

depths = [
    0, 5, 10, 15, 20, 25, 30, 35, 40, 45,
    50, 55, 60, 65, 70, 75, 80, 85, 90, 95,
    100, 125, 150, 175, 200, 225, 250, 275, 300, 325,
    350, 375, 400, 425, 450, 475, 500, 550, 600, 650,
    700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150,
    1200, 1250, 1300, 1350, 1400, 1450, 1500
]


def get_plot(map_type, lat, lon, time=-1):
    time = int(round(float(time)))
    lat = int(round(float(lat) / SCALE))
    lon = int(round(float(lon) / SCALE))

    data_raw = np.load(f"data/{map_type}/{time}.npy")[:, lat, lon]
    data = []

    for i in range(len(data_raw)):
        if np.isnan(data_raw[i]):
            continue

        data.append({"y": depths[i], "x": data_raw[i]})

    return data
