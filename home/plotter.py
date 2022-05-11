import numpy as np

from install import SCALE


def get_plot(map_type, lat, lon, time=-1):
    time = int(round(float(time)))
    lat = int(round(float(lat)/SCALE))
    lon = int(round(float(lon)/SCALE))

    data_raw = np.load(f"data/{map_type}/{time}.npy")[:, lat, lon]
    data = {}

    for i in range(len(data_raw)):
        if np.isnan(data_raw[i]):
            continue
        data[f"{i*(1500/57)}"] = data_raw[i]

    return data
