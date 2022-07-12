import math
import pathlib
import sys

import numpy as np
import xarray as xr
import cv2

depths = [
    0, 5, 10, 15, 20, 25, 30, 35, 40, 45,
    50, 55, 60, 65, 70, 75, 80, 85, 90, 95,
    100, 125, 150, 175, 200, 225, 250, 275, 300, 325,
    350, 375, 400, 425, 450, 475, 500, 550, 600, 650,
    700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150,
    1200, 1250, 1300, 1350, 1400, 1450, 1500
]

TIME_RESOLUTION = 1
DEPTH_RESOLUTION = 5

SCALE = 2

size = (1440 * SCALE, 720 * SCALE)

# colors = [[2, 0, 0], [28, 5, 0], [100, 57, 0], [196, 158, 16], [175, 229, 145], [220, 251, 219]] sea

colors = [*reversed([[*reversed(c)] for c in
                     [[134, 217, 240], [92, 182, 247], [62, 171, 250], [5, 145, 247], [0, 0, 250]]])]


def calculate_sound_speed(t, s, d, lat):
    return 1402.5 + (5 * t) - (0.0544 * t * t) + (0.00021 * t * t * t) + (1.33 * s) - (0.0123 * s * t) + \
           (0.000087 * s * t * t) + (0.0156 * d) + (0.000000255 * d * d) - (0.0000000000073 * d * d * d) + \
           (1.2 * d * (lat - 45)) - (0.00000000000095 * t * d * d * d) + (0.0000003 * t * t * d) + (0.0000143 * s * d)


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
        break


def save_current_as_np():
    pathlib.Path("data/c_an").mkdir(parents=True, exist_ok=True)

    data_raw = xr.open_dataset("netcdf/cur_spd_dir.nc", decode_times=False)

    for j in range(12):
        arrays = []
        for k in range(50):
            numpy_array = data_raw.get("SPEED").isel(ST_OCEAN=[k], TIME=[j]).values[0, 0]
            cv2.flip(numpy_array, 0, dst=numpy_array)
            numpy_array = cv2.resize(numpy_array, (1140, 720), interpolation=cv2.INTER_CUBIC)

            arrays.append(numpy_array)

        np.save(f"data/c_an/{j}.npy", np.array(arrays, dtype=np.float32))


def save_sound_speed():
    pathlib.Path("data/s_nd").mkdir(parents=True, exist_ok=True)

    for j in range(12):
        print(j)
        sal = np.load(f"data/s_an/{j}.npy", mmap_mode="r")
        tmp = np.load(f"data/t_an/{j}.npy", mmap_mode="r")
        dep = np.ones(sal.shape) * depths[j]
        lat = np.tile(np.arange(0, sal.shape[2] / 4, 0.25), (sal.shape[0], sal.shape[1], 1))

        np.save(f"data/s_nd/{j}.npy", calculate_sound_speed(tmp, sal, dep, lat))


def generate_legend(dataset_path, data_variable):
    pathlib.Path(f"media/{data_variable}/legend").mkdir(parents=True, exist_ok=True)

    data_raw = xr.open_dataset(dataset_path, decode_times=False)
    grad = cv2.flip(cv2.resize(cv2.imread("data/legend.png"), (1000, 20)), 1)

    for k in range(len(data_raw.depth)):
        numpy_array = data_raw.get(data_variable).isel(depth=[k]).values[0, 0]

        min_val = np.nanmin(numpy_array)
        max_val = np.nanmax(numpy_array)

        steps = 6
        image = np.copy(grad)

        for d in range(steps + 1):
            val = round(min_val + ((max_val - min_val) / steps * d))
            x = round(10 + (d * grad.shape[1] / steps))

            image = cv2.putText(image, str(val), (x, (grad.shape[0] >> 1) + 5),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.imwrite(f"media/{data_variable}/legend/{k}.png", image)

    cv2.waitKey()


def generate_bath_legend():
    numpy_array = np.load("data/bath.npy")

    numpy_array[numpy_array >= 0] = 0

    numpy_array *= -1

    min_val = np.nanmin(numpy_array)
    max_val = np.nanmax(numpy_array)

    steps = 6

    grad = cv2.resize(cv2.imread("data/bath_legend.png"), (1000, 20))

    for d in range(steps + 1):
        val = round(min_val + ((max_val - min_val) / steps * d))
        x = round(10 + (d * grad.shape[1] / steps))

        grad = cv2.putText(grad, str(val), (x, (grad.shape[0] >> 1) + 5),
                           cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imwrite(f"media/bath/legend/{0}.png", grad)


def get_path(x1, y1, th, length, scale):
    th = math.radians(th)

    x2 = x1 + length * math.cos(th) * 8
    y2 = y1 + length * math.sin(th)  * 8

    return (round(x1*scale[0]), round(y1*scale[1])), (round(x2*scale[0]), round(y2*scale[1]))


def generate_current():
    pathlib.Path("media/c_an").mkdir(parents=True, exist_ok=True)

    data_cur = xr.open_dataset("netcdf/cur_spd_dir.nc", decode_times=False)
    data_dir = xr.open_dataset("netcdf/current_dir.nc", decode_times=False)

    for j in range(12):
        for k in range(50):
            numpy_array = data_cur.get("SPEED").isel(ST_OCEAN=[k], TIME=[j]).values[0, 0]
            dir_array = data_dir.get("DIR").isel(ST_OCEAN=[k], TIME=[j]).values[0, 0]

            min_val = np.nanmin(numpy_array)
            max_val = np.nanmax(numpy_array)

            image = np.ones((*numpy_array.shape, 3), dtype=np.uint8) * 255
            paths = []

            for lat in range(len(numpy_array)):
                for lng in range(len(numpy_array[0])):
                    if not np.isnan(numpy_array[lat, lng]):
                        image[lat, lng] = convert_to_rgb(minval=min_val, maxval=max_val, val=numpy_array[lat, lng])
                        if not np.isnan(dir_array[lat, lng]) and lat % 5 == 0 and lng % 5 == 0:
                            scale = size[0] / numpy_array.shape[1], size[1] / numpy_array.shape[0]
                            length = numpy_array[lat, lng] / max_val
                            paths.append(get_path(lng, lat, dir_array[lat, lng], length, scale))

            image = cv2.resize(image, size, interpolation=cv2.INTER_CUBIC)

            for path in paths:
                image = cv2.arrowedLine(image, path[0], path[1], (0, 0, 0), 4, 16, shift=0, tipLength=0.5)

            image = cv2.flip(image, -1)

            cv2.imwrite(f"media/c_an/{j}-{k}.png", image)
            print(f"media/c_nd/{j}-{k}.png")


def main():
    numpy_array = np.load("data/bath.npy")

    numpy_array[numpy_array >= 0] = 0

    min_val = np.nanmin(numpy_array)
    max_val = np.nanmax(numpy_array)

    image = np.ones((*numpy_array.shape, 3), dtype=np.uint8) * 255

    for lat in range(len(numpy_array)):
        for lng in range(len(numpy_array[0])):
            if numpy_array[lat, lng] == 0:
                image[lat, lng] = [74, 240, 212]
            else:
                image[lat, lng] = convert_to_rgb(minval=min_val, maxval=max_val, val=numpy_array[lat, lng])

    cv2.imwrite("media/bath/0-0.png", image)
    # generate_legend("netcdf/woa_temp.nc", "t_an")
    # create_images("netcdf/woa_temp.nc", "t_an")


if __name__ == '__main__':
    save_current_as_np()
    # generate_bath_legend()
    # import gzip
    #
    # for map_type in ["t_an", "s_nd"]:
    #     for d in range(12):
    #         path = rf"D:/Data/Trebuchet/seamap-backend/data/{map_type}/{d}.npy"
    #         pathlib.Path(f"data-c/{map_type}").mkdir(parents=True, exist_ok=True)
    #         f = gzip.GzipFile(f'data-c/{map_type}/{d}.npy.gz', "w")
    #         np.save(f, np.asarray(np.load(path, allow_pickle=True) * 100, dtype=np.int32))
    #         f.close()
    #         print(path)

    # save_sound_speed()
    # main()
    # d = np.load("data/bath.npy")
    #
    # image = np.zeros((*d.shape, 4), dtype=np.uint8)
    #
    # image[d >= 0] = [*reversed([179, 245, 66]), 255]
    #
    # # image = cv2.flip(d, 0)
    #
    # # np.save("data/bath.npy", image)
    #
    # cv2.imwrite("media/map.png", image)
