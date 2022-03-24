import io
import textwrap

import matplotlib.pyplot as plt
import xarray as xr


def _get_units_from_attrs(da):
    """Extracts and formats the unit/units from a attributes."""
    units = " [{}]"

    if da.attrs.get("units"):
        units = units.format(da.attrs["units"])
    elif da.attrs.get("unit"):
        units = units.format(da.attrs["unit"])
    else:
        units = ""
    return units


def label_from_attrs(da, extra=""):
    """Makes informative labels if variable metadata (attrs) follows
    CF conventions."""

    if da.attrs.get("long_name"):
        name = da.attrs["long_name"]
    elif da.attrs.get("standard_name"):
        name = da.attrs["standard_name"]
    elif da.name is not None:
        name = da.name
    else:
        name = ""

    units = _get_units_from_attrs(da)

    # Treat `name` differently if it's a latex sequence
    if name.startswith("$") and (name.count("$") % 2 == 0):
        return "$\n$".join(
            textwrap.wrap(name + extra + units, 60, break_long_words=False)
        )
    else:
        return "\n".join(textwrap.wrap(name + extra + units, 30))


def plot(darray):
    dim = darray.dims[0]
    xplt = darray[dim]
    yplt = darray

    # Remove pd.Intervals if contained in xplt.values and/or yplt.values.
    xplt_val, yplt_val = xplt.values, yplt.values
    # xplt_val = np.array([x.mid for x in xplt_val])

    xlabel = label_from_attrs(xplt)
    ylabel = label_from_attrs(yplt)

    fig = plt.figure()

    plt.plot(xplt_val, yplt_val)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(darray._title_for_slice())

    f = io.BytesIO()

    fig.savefig(f, format='svg', bbox_inches="tight")

    return f.getvalue()


def get_plot(lat, lon, time):
    to_plot = data_raw.get("s_an").isel(lat=lat, lon=lon, time=time).squeeze()

    if "time" in to_plot:
        del to_plot["time"]

    print(plot(to_plot))
