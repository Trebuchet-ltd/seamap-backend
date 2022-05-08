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

colors = [[148, 0, 211], [75, 0, 130], [0, 0, 255], [0, 255, 0],
          [255, 255, 0], [255, 127, 0], [255, 0, 0]]


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

            min_val = np.nanmin(numpy_array)
            max_val = np.nanmax(numpy_array)

            image = np.ones((*numpy_array.shape, 3), dtype=np.uint8) * 255

            for lat in range(len(numpy_array)):
                for lng in range(len(numpy_array[0])):
                    if not np.isnan(numpy_array[lat, lng]):
                        image[lat, lng] = convert_to_rgb(minval=min_val, maxval=max_val, val=numpy_array[lat, lng])

            image = cv2.flip(image, 0)
            image = cv2.resize(image, size, interpolation=cv2.INTER_CUBIC)

            cv2.imwrite(f"media/{data_variable}/{j}-{k}.png", image)
            print(f"media/{data_variable}/{j}-{k}.png")


def main():
    create_images("netcdf/woa_temp.nc", "t_an")


if __name__ == '__main__':
    main()
