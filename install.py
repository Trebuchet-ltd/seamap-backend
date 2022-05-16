import pathlib
import sys

import numpy as np
import xarray as xr
import cv2

LAT_RESOLUTION = 0.25
LON_RESOLUTION = 0.25
TIME_RESOLUTION = 1
DEPTH_RESOLUTION = 5

SCALE = 2

size = (1440 * SCALE, 720 * SCALE)

# colors = [[148, 0, 211], [75, 0, 130], [0, 0, 255], [0, 255, 0],
#           [255, 255, 0], [255, 127, 0], [255, 0, 0]]

colors = [[*reversed(c)] for c in
          [[164, 235, 245], [134, 217, 240], [92, 182, 247], [62, 171, 250], [5, 145, 247], [0, 0, 250]]]


def convert_to_rgb(val, minval, maxval):
    if np.isnan(val):
        return [255, 255, 255]

    i_f = float(val - minval) / float(maxval - minval) * (len(colors) - 1)
    i, f = int(i_f // 1), i_f % 1  # Split into whole & fractional parts.

    # Does it fall exactly on one of the color points?
    if f < sys.float_info.epsilon:
        return colors[i]
    else:
        (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i + 1]
        return [int(r1 + f * (r2 - r1)), int(g1 + f * (g2 - g1)), int(b1 + f * (b2 - b1))]


def create_images(dataset_path, data_variable):
    pathlib.Path(f"media/{data_variable}").mkdir(parents=True, exist_ok=True)
    data_raw = xr.open_dataset(dataset_path, decode_times=False)

    for j in range(12):
        for k in range(57):
            numpy_array = data_raw.get(data_variable).isel(depth=[k], time=[j]).values[0, 0]

            numpy_array[numpy_array >= 0] = np.nan

            min_val = np.nanmin(numpy_array)
            max_val = np.nanmax(numpy_array)

            image = np.zeros((*numpy_array.shape, 3), dtype=np.uint8)

            for lat in range(len(numpy_array)):
                for lng in range(len(numpy_array[0])):
                    if not np.isnan(numpy_array[lat, lng]):
                        image[lat, lng] = convert_to_rgb(minval=min_val, maxval=max_val, val=numpy_array[lat, lng])

            image = cv2.flip(image, 0)
            image = cv2.resize(image, size, interpolation=cv2.INTER_CUBIC)

            image[image == [0, 0, 0]] = [74, 240, 212]

            cv2.imwrite(f"media/{data_variable}/{j}-{k}.png", image)
            print(f"media/{data_variable}/{j}-{k}.png")


def save_as_np(dataset_path, data_variable):
    pathlib.Path(f"data/{data_variable}").mkdir(parents=True, exist_ok=True)

    data_raw = xr.open_dataset(dataset_path, decode_times=False)

    for j in range(12):
        arrays = []
        for k in range(57):
            numpy_array = data_raw.get(data_variable).isel(depth=[k], time=[j]).values[0, 0]
            cv2.flip(numpy_array, 0, dst=numpy_array)

            arrays.append(numpy_array)

        np.save(f"data/{data_variable}/{j}.npy", np.array(arrays, dtype=np.float32))


def generate_legend(dataset_path, data_variable):
    pathlib.Path(f"media/{data_variable}/legend").mkdir(parents=True, exist_ok=True)

    data_raw = xr.open_dataset(dataset_path, decode_times=False)
    grad = cv2.imread("data/legend.png")

    for k in range(len(data_raw.depth)):
        numpy_array = data_raw.get(data_variable).isel(depth=[k]).values[0, 0]

        min_val = np.nanmin(numpy_array)
        max_val = np.nanmax(numpy_array)

        steps = 20
        image = np.copy(grad)

        for d in range(steps):
            val = round(min_val + ((max_val - min_val) / steps * d), 1)
            image = cv2.putText(image, str(val), (round(5 + (d * grad.shape[1] / steps)), grad.shape[0] >> 1),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0, 0, 0), 2, cv2.LINE_AA)

        cv2.imwrite(f"media/{data_variable}/legend/{k}.png", image)

    cv2.waitKey()


def main():
    numpy_array = np.load("data/bath.npy", mmap_mode="r")

    min_val = np.nanmin(numpy_array)
    max_val = np.nanmax(numpy_array)

    image = np.ones((*numpy_array.shape, 3), dtype=np.uint8) * 255

    for lat in range(len(numpy_array)):
        for lng in range(len(numpy_array[0])):
            if not np.isnan(numpy_array[lat, lng]):
                image[lat, lng] = convert_to_rgb(minval=min_val, maxval=max_val, val=numpy_array[lat, lng])

    cv2.imwrite("media/bath/0-0.png", image)
    # generate_legend("netcdf/woa_salt.nc", "s_an")
    # data_raw = np.load(f"data/s_an/0.npy")[1]
    #
    # cv2.imshow("aa", data_raw)
    # cv2.waitKey()


if __name__ == '__main__':
    main()
    # d = xr.open_dataset("netcdf/GEBCO_2021_sub_ice_topo.nc", decode_times=False)
    # d = cv2.resize(d.get("elevation").values, size, interpolation=cv2.INTER_AREA)
    #
    # image = np.zeros((*d.shape, 4), dtype=np.uint8)
    #
    # image[d >= 0] = [74, 240, 212, 255]

    # image = cv2.flip(d, 0)
    #
    # np.save("data/bath.npy", image)
    #
    # cv2.imwrite("media/map.png", image)
