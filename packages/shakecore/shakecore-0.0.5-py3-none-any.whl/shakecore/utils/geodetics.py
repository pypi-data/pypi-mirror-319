import contextily as ctx
import matplotlib.pyplot as plt
import numpy as np

from matplotlib_scalebar.scalebar import ScaleBar
from obspy.geodetics import degrees2kilometers, gps2dist_azimuth, locations2degrees
from pyproj import Transformer
from rasterio.enums import Resampling
from scipy.interpolate import griddata, interpn


def add_basemap(
    ax,
    lon_min,
    lon_max,
    lat_min,
    lat_max,
    zoom="auto",
    source=None,
    interpolation="bilinear",
    attribution=None,
    attribution_size=8,
    reset_extent=True,
    crs=None,
    resampling=Resampling.bilinear,
    zoom_adjust=None,
    **extra_imshow_args,
):
    transformer = Transformer.from_crs(
        crs_from="EPSG:4326", crs_to="EPSG:3857", always_xy=True
    )

    x_min, y_min = transformer.transform(lon_min, lat_min)
    x_max, y_max = transformer.transform(lon_max, lat_max)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ctx.add_basemap(
        ax,
        zoom=zoom,
        source=source,
        interpolation=interpolation,
        attribution=attribution,
        attribution_size=attribution_size,
        reset_extent=reset_extent,
        crs=crs,
        resampling=resampling,
        zoom_adjust=zoom_adjust,
        **extra_imshow_args,
    )

    return transformer


def add_ticks(
    ax,
    unit="degree",  # unit: 'degree', 'km', 'm'
    interval=0.1,
    rotation_x=0,
    rotation_y=0,
):
    # determine the number of decimal places to round to based on the interval
    interval_str = str(interval)
    if "." in interval_str:
        decimal_part = interval_str.split(".")[1]
        nround = len(decimal_part)
        if unit == "latlon":
            nround += 1
    else:
        nround = 0

    # get the current x and y limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    if unit == "degree":
        transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

        x_ticks = np.linspace(
            xlim[0], xlim[1], int((xlim[1] - xlim[0]) / (interval * 111320))
        )
        y_ticks = np.linspace(
            ylim[0], ylim[1], int((ylim[1] - ylim[0]) / (interval * 111320))
        )

        # convert Web Mercator coordinates to latlon
        x_labels = [
            f"{transformer.transform(tick, ylim[0])[0]:.{nround}f}" for tick in x_ticks
        ]
        y_labels = [
            f"{transformer.transform(xlim[0], tick)[1]:.{nround}f}" for tick in y_ticks
        ]

        # set the tick labels
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([f"{label}°" for label in x_labels])
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([f"{label}°" for label in y_labels])

    elif unit in ["km", "m"]:
        x_ticks = (
            plt.MultipleLocator(interval * 1000).tick_values(*xlim)
            if unit == "km"
            else plt.MultipleLocator(interval).tick_values(*xlim)
        )
        y_ticks = (
            plt.MultipleLocator(interval * 1000).tick_values(*ylim)
            if unit == "km"
            else plt.MultipleLocator(interval).tick_values(*ylim)
        )

        # set the tick labels
        if unit == "km":
            xtick_labels = [f"{(tick - xlim[0]) / 1000:.{nround}f}" for tick in x_ticks]
            ytick_labels = [f"{(tick - ylim[0]) / 1000:.{nround}f}" for tick in y_ticks]
        else:
            xtick_labels = [f"{tick - xlim[0]:.{nround}f}" for tick in x_ticks]
            ytick_labels = [f"{tick - ylim[0]:.{nround}f}" for tick in y_ticks]

        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)
        ax.set_xticklabels(xtick_labels)
        ax.set_yticklabels(ytick_labels)

    # rotate the tick labels
    plt.setp(ax.get_xticklabels(), rotation=rotation_x)
    plt.setp(ax.get_yticklabels(), rotation=rotation_y)

    # set raw x and y limits
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)


def add_scale(
    ax,
    location="lower right",
    length_fraction=0.1,
    color="black",
    box_alpha=0.5,
    box_color="white",
    scale_loc="top",
    font_properties={"size": 10},
):
    scalebar = ScaleBar(
        dx=1,
        units="m",
        dimension="si-length",
        length_fraction=length_fraction,
        color=color,
        box_alpha=box_alpha,
        box_color=box_color,
        scale_loc=scale_loc,
        font_properties=font_properties,
    )
    scalebar.location = location
    ax.add_artist(scalebar)


def utm_2_latlon(utm_x, utm_y, source_epsg, dest_epsg="EPSG:4326"):
    transformer = Transformer.from_crs(source_epsg, dest_epsg)
    lat, lon = transformer.transform(utm_x, utm_y)

    return lat, lon


def latlon_2_utm(lat, lon, dest_epsg, source_epsg="EPSG:4326"):
    transformer = Transformer.from_crs(source_epsg, dest_epsg)
    utm_x, utm_y = transformer.transform(lat, lon)

    return utm_x, utm_y


def latlon_2_dist(lat1, lon1, lat2, lon2, method="WGS84"):
    if method == "WGS84":
        dist, _, _ = gps2dist_azimuth(lat1, lon1, lat2, lon2)  # use WGS84, unit: meters
    elif method == "spherical":
        dist = (
            degrees2kilometers(locations2degrees(lat1, lon1, lat2, lon2)) * 1e3
        )  # use spherical earth, unit: meters

    return dist


def latlon_2_az(lat1, lon1, lat2, lon2):
    _, az, _ = gps2dist_azimuth(lat1, lon1, lat2, lon2)  # use WGS84, unit: degrees

    return az


def latlon_2_baz(lat1, lon1, lat2, lon2):
    _, _, baz = gps2dist_azimuth(lat1, lon1, lat2, lon2)  # use WGS84, unit: degrees

    return baz


def projection(A, B, C):
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)

    if A.ndim == 1:
        A = A.reshape(1, -1)
    if B.ndim == 1:
        B = B.reshape(1, -1)
    if C.ndim == 1:
        C = C.reshape(1, -1)
        ndim = 1
    else:
        ndim = 2

    AB = B - A
    AC = C - A.reshape(1, -1)

    dot_product = np.sum(AC * AB, axis=1)
    length_squared = np.sum(AB**2)

    projection_length = dot_product / length_squared
    D = A + projection_length.reshape(-1, 1) * AB

    if ndim == 1:
        D = D[0]

    return D


def vel2tz(depth, vel):
    """
    Given instantaneous velocity versus depth, compute a two-way time-depth curve.

    Parameters:
    depth (numpy array): A 1D array of depth values.
    vel (numpy array): A 1D array of velocity values corresponding to the depth values.

    Returns:
    tz (numpy array): A 1D array of two-way travel times corresponding to the depth values.
    """
    # Check that depth and velocity arrays have the same length
    if len(depth) != len(vel):
        raise ValueError("Depth and velocity arrays must have the same length")

    # Calculate the travel time for each depth interval
    dt = np.diff(depth) / vel[:-1]

    # Compute the cumulative sum of travel times
    t = np.cumsum(dt)

    # Add the initial time (0 at depth 0)
    t = np.insert(t, 0, 0)

    # Double the time to get the two-way travel time
    t = 2 * t

    return t, depth


class Model2D:
    def __init__(self, x, z, value):
        self.init(x, z, value)

    def init(self, x, z, value):
        sort_indices = np.lexsort((z, x))  # sort by x, z
        self.x = x[sort_indices]
        self.z = z[sort_indices]
        self.value = value[sort_indices]
        self.x_min = np.nanmin(x)
        self.x_max = np.nanmax(x)
        self.z_min = np.nanmin(z)
        self.z_max = np.nanmax(z)
        self.value_min = np.nanmin(value)
        self.value_max = np.nanmax(value)
        self.x_axis, self.x_index = np.unique(x, return_inverse=True)
        self.z_axis, self.z_index = np.unique(z, return_inverse=True)

        if np.isnan(self.value).any():
            self.include_nan = True
        else:
            self.include_nan = False

    def __str__(self):
        info = (
            "* Model2D: \n"
            f"            x_min: {self.x_min}\n"
            f"            x_max: {self.x_max}\n"
            f"            z_min: {self.z_min}\n"
            f"            z_max: {self.z_max}\n"
            f"        value_min: {self.value_min}\n"
            f"        value_max: {self.value_max}\n"
            f"        value_num: {len(self.value)} =? {len(self.x_axis)} * {len(self.z_axis)} || (nx_axis * nz_axis)\n"
        )

        return info

    def __repr__(self):
        return str(self)

    def save(self, filename):
        np.savez(filename, x=self.x, z=self.z, value=self.value)

    def griddata(
        self,
        x_min,
        x_max,
        dx,
        z_min,
        z_max,
        dz,
        method="linear",  # 'linear','nearest','cubic'
        fill_value=np.nan,
        handle_nan=True,
    ):
        x = np.arange(x_min, x_max + dx, dx)
        z = np.arange(z_min, z_max + dz, dz)

        x_new, z_new = np.meshgrid(x, z, indexing="ij")

        points = np.vstack([self.x, self.z]).T

        value_new = griddata(
            points, self.value, (x_new, z_new), method=method, fill_value=fill_value
        )

        # perform nearest neighbor interpolation for NaN values
        if np.isnan(value_new).any() and handle_nan:
            nan_indices = np.isnan(value_new)
            value_nearest = griddata(
                points,
                self.value,
                (x_new[nan_indices], z_new[nan_indices]),
                method="nearest",
            )
            value_new[nan_indices] = value_nearest

        if np.isnan(value_new).any():
            self.include_nan = True

        self.init(x_new.flatten(), z_new.flatten(), value_new.flatten())

    def interpndata(
        self,
        x_min,
        x_max,
        dx,
        z_min,
        z_max,
        dz,
        method="linear",  # “linear”, “nearest”, “slinear”, “cubic”, “quintic”, “pchip”
        bounds_error=False,
        fill_value=np.nan,
    ):
        x = np.arange(x_min, x_max + dx, dx)
        z = np.arange(z_min, z_max + dz, dz)
        grid_x, grid_z = np.meshgrid(x, z, indexing="ij")

        points = (self.x_axis, self.z_axis)
        values = self.value.reshape((len(self.x_axis), len(self.z_axis)))

        value_new = interpn(
            points,
            values,
            (grid_x, grid_z),
            method=method,
            bounds_error=bounds_error,
            fill_value=fill_value,
        )

        if np.isnan(value_new).any():
            self.include_nan = True

        self.init(grid_x.flatten(), grid_z.flatten(), value_new.flatten())

    def layer(
        self,
        x,
        z_num=100,
        method="linear",
        plot=False,
        figsize=(10, 6),
        show=True,
        save_path=None,
        dpi=100,
    ):
        # generate grid axis
        z_axis = np.linspace(self.z_min, self.z_max, z_num)
        grid_x, grid_z = np.meshgrid([x], z_axis, indexing="ij")

        # interpolate
        points = (self.x_axis, self.z_axis)
        values = self.value.reshape((len(self.x_axis), len(self.z_axis)))
        z_values = interpn(
            points,
            values,
            (grid_x, grid_z),
            method=method,
            bounds_error=False,
            fill_value=None,
        ).flatten()

        # plot
        if plot:
            fig, ax = plt.subplots(figsize=figsize)
            ax.plot(z_values, z_axis, "o-", color="red")
            ax.set_xlabel("Value")
            ax.set_ylabel("Z Axis")
            ax.invert_yaxis()
            ax.grid()

            if show:
                plt.show()
            else:
                plt.close(fig)
            if save_path is not None:
                fig.savefig(save_path, dpi=dpi)

        return z_values, z_axis

    def plot(
        self,
        cmap="jet_r",
        clip=[None, None],
        figsize=(10, 6),
        show=True,
        save_path=None,
        dpi=100,
    ):
        fig, ax = plt.subplots(figsize=figsize)
        values = self.value.reshape((len(self.x_axis), len(self.z_axis)))
        im = ax.imshow(
            values.T,
            origin="lower",
            aspect="auto",
            cmap=cmap,
            extent=[self.x_min, self.x_max, self.z_min, self.z_max],
        )

        if clip[0] is not None and clip[1] is not None:
            im.set_clim(clip)

        ax.invert_yaxis()
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Z Axis")
        cbar = plt.colorbar(im, orientation="vertical", ax=ax)
        cbar.set_label("Value")

        if show:
            plt.show()
        else:
            plt.close(fig)
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi)


class Model3D:
    def __init__(self, x, y, z, value):
        self.init(x, y, z, value)

    def init(self, x, y, z, value):
        sort_indices = np.lexsort((z, y, x))  # sort by x, y, z
        self.x = x[sort_indices]
        self.y = y[sort_indices]
        self.z = z[sort_indices]
        self.value = value[sort_indices]
        self.x_min = np.nanmin(x)
        self.x_max = np.nanmax(x)
        self.y_min = np.nanmin(y)
        self.y_max = np.nanmax(y)
        self.z_min = np.nanmin(z)
        self.z_max = np.nanmax(z)
        self.value_min = np.nanmin(value)
        self.value_max = np.nanmax(value)
        self.x_axis, self.x_index = np.unique(x, return_inverse=True)
        self.y_axis, self.y_index = np.unique(y, return_inverse=True)
        self.z_axis, self.z_index = np.unique(z, return_inverse=True)

        if np.isnan(self.value).any():
            self.include_nan = True
        else:
            self.include_nan = False

    def __str__(self):
        info = (
            "* Model3D: \n"
            f"            x_min: {self.x_min}\n"
            f"            x_max: {self.x_max}\n"
            f"            y_min: {self.y_min}\n"
            f"            y_max: {self.y_max}\n"
            f"            z_min: {self.z_min}\n"
            f"            z_max: {self.z_max}\n"
            f"      include_nan: {self.include_nan}\n"
            f"        value_min: {self.value_min}\n"
            f"        value_max: {self.value_max}\n"
            f"        value_num: {len(self.value)} =? {len(self.x_axis)} * {len(self.y_axis)} * {len(self.z_axis)} || (nx_axis * ny_axis * nz_axis)\n"
        )

        return info

    def __repr__(self):
        return str(self)

    def save(self, filename):
        np.savez(filename, x=self.x, y=self.y, z=self.z, value=self.value)

    def griddata(
        self,
        x_min,
        x_max,
        dx,
        y_min,
        y_max,
        dy,
        z_min,
        z_max,
        dz,
        method="linear",  # 'linear','nearest','cubic'
        fill_value=np.nan,
        handle_nan=True,
    ):
        x = np.arange(x_min, x_max + dx, dx)
        y = np.arange(y_min, y_max + dy, dy)
        z = np.arange(z_min, z_max + dz, dz)

        x_new, y_new, z_new = np.meshgrid(x, y, z, indexing="ij")

        points = np.vstack([self.x, self.y, self.z]).T

        value_new = griddata(
            points,
            self.value,
            (x_new, y_new, z_new),
            method=method,
            fill_value=fill_value,
        )

        # perform nearest neighbor interpolation for NaN values
        if np.isnan(value_new).any() and handle_nan:
            nan_indices = np.isnan(value_new)
            value_nearest = griddata(
                points,
                self.value,
                (x_new[nan_indices], y_new[nan_indices], z_new[nan_indices]),
                method="nearest",
            )
            value_new[nan_indices] = value_nearest

        if np.isnan(value_new).any():
            self.include_nan = True

        self.init(
            x_new.flatten(), y_new.flatten(), z_new.flatten(), value_new.flatten()
        )

    def interpndata(
        self,
        x_min,
        x_max,
        dx,
        y_min,
        y_max,
        dy,
        z_min,
        z_max,
        dz,
        method="linear",  # “linear”, “nearest”, “slinear”, “cubic”, “quintic”, “pchip”
        bounds_error=False,
        fill_value=np.nan,
    ):
        x = np.arange(x_min, x_max + dx, dx)
        y = np.arange(y_min, y_max + dy, dy)
        z = np.arange(z_min, z_max + dz, dz)
        grid_x, grid_y, grid_z = np.meshgrid(x, y, z, indexing="ij")

        points = (self.x_axis, self.y_axis, self.z_axis)
        values = self.value.reshape(
            (len(self.x_axis), len(self.y_axis), len(self.z_axis))
        )

        value_new = interpn(
            points,
            values,
            (grid_x, grid_y, grid_z),
            method=method,
            bounds_error=bounds_error,
            fill_value=fill_value,
        )

        if np.isnan(value_new).any():
            self.include_nan = True

        self.init(
            grid_x.flatten(), grid_y.flatten(), grid_z.flatten(), value_new.flatten()
        )

    # layer
    def layer(
        self,
        point,
        mode="num",  # 'num' or "interval"
        dz=10,
        z_num=100,
        method="linear",
        plot=False,
        figsize=(10, 6),
        show=True,
        save_path=None,
        dpi=100,
    ):
        x_point, y_point = point

        # generate grid axis
        if mode == "num":
            z_axis = np.linspace(self.z_min, self.z_max, z_num)
        elif mode == "interval":
            z_axis = np.arange(self.z_min, self.z_max, dz)
        grid_x, grid_y, grid_z = np.meshgrid(
            [x_point], [y_point], z_axis, indexing="ij"
        )

        # interpolate
        points = (self.x_axis, self.y_axis, self.z_axis)
        values = self.value.reshape(
            (len(self.x_axis), len(self.y_axis), len(self.z_axis))
        )
        z_values = interpn(
            points,
            values,
            (grid_x, grid_y, grid_z),
            method=method,
            bounds_error=False,
            fill_value=None,
        ).flatten()

        # plot
        if plot:
            fig, ax = plt.subplots(figsize=figsize)
            ax.plot(z_values, z_axis, "o-", color="red")
            ax.set_xlabel("Value")
            ax.set_ylabel("Z Axis")
            ax.invert_yaxis()
            ax.grid()

            if show:
                plt.show()
            else:
                plt.close(fig)
            if save_path is not None:
                fig.savefig(save_path, dpi=dpi)

        return z_values, z_axis

    # horizontal slice
    def slice(
        self,
        z,
        mode="num",  # 'num' or "interval"
        dx=10,
        dy=10,
        x_num=100,
        y_num=100,
        method="linear",
        fill_value=np.nan,
        plot=False,
        cmap="jet_r",
        clip=[None, None],
        figsize=(10, 6),
        show=True,
        save_path=None,
        dpi=100,
    ):
        # generate grid axis
        if mode == "num":
            x_axis = np.linspace(self.x_min, self.x_max, x_num)
            y_axis = np.linspace(self.y_min, self.y_max, y_num)
        elif mode == "interval":
            x_axis = np.arange(self.x_min, self.x_max, dx)
            y_axis = np.arange(self.y_min, self.y_max, dy)
        grid_x, grid_y, grid_z = np.meshgrid(x_axis, y_axis, z, indexing="ij")

        # interpolate
        points = (self.x_axis, self.y_axis, self.z_axis)
        values = self.value.reshape(
            (len(self.x_axis), len(self.y_axis), len(self.z_axis))
        )
        slice_values = interpn(
            points,
            values,
            (grid_x, grid_y, grid_z),
            method=method,
            bounds_error=False,
            fill_value=fill_value,
        )[:, :, 0]

        # plot
        if plot:
            fig, ax = plt.subplots(figsize=figsize)
            im = ax.imshow(
                slice_values.T,
                origin="lower",
                aspect="auto",
                cmap=cmap,
                extent=[self.x_min, self.x_max, self.y_min, self.y_max],
            )

            if clip[0] is not None and clip[1] is not None:
                im.set_clim(clip)

            ax.set_xlabel("X Axis")
            ax.set_ylabel("Y Axis")
            cbar = plt.colorbar(im, orientation="vertical", ax=ax)
            cbar.set_label("Value")

            if show:
                plt.show()
            else:
                plt.close(fig)
            if save_path is not None:
                fig.savefig(save_path, dpi=dpi)

        return slice_values, x_axis, y_axis

    # vertical slice
    def profile(
        self,
        point1,
        point2,
        mode="num",  # 'num' or "interval"
        d_dist=10,
        dz=10,
        dist_num=100,
        z_num=100,
        method="linear",
        fill_value=np.nan,
        plot=False,
        cmap="jet_r",
        clip=[None, None],
        figsize=(10, 6),
        show=True,
        save_path=None,
        dpi=100,
    ):
        x1, y1 = point1
        x2, y2 = point2

        # generate grid axis
        if mode == "num":
            x_axis = np.linspace(x1, x2, dist_num)
            y_axis = np.linspace(y1, y2, dist_num)
            z_axis = np.linspace(self.z_min, self.z_max, z_num)
            distances = np.sqrt((x_axis - x1) ** 2 + (y_axis - y1) ** 2)
        elif mode == "interval":
            theta = np.arctan2(y2 - y1, x2 - x1)
            distances = np.arange(0, np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), d_dist)
            x_axis = x1 + distances * np.cos(theta)
            y_axis = y1 + distances * np.sin(theta)
            z_axis = np.arange(self.z_min, self.z_max, dz)

        grid_x, grid_y, grid_z = np.meshgrid(x_axis, y_axis, z_axis, indexing="ij")

        # interpolate
        points = (self.x_axis, self.y_axis, self.z_axis)
        values = self.value.reshape(
            (len(self.x_axis), len(self.y_axis), len(self.z_axis))
        )
        profile_values = interpn(
            points,
            values,
            (grid_x[:, 0, :], grid_y[0, :, :], grid_z[0, 0, :]),
            method=method,
            bounds_error=False,
            fill_value=fill_value,
        )

        # plot
        if plot:
            fig, ax = plt.subplots(figsize=figsize)
            im = ax.imshow(
                profile_values.T,
                origin="lower",
                aspect="auto",
                cmap=cmap,
                extent=[0, distances[-1], self.z_min, self.z_max],
            )

            if clip[0] is not None and clip[1] is not None:
                im.set_clim(clip)

            ax.invert_yaxis()
            ax.set_xlabel("Distance along the Profile")
            ax.set_ylabel("Z Axis")
            cbar = plt.colorbar(im, orientation="vertical", ax=ax)
            cbar.set_label("Value")

            if show:
                plt.show()
            else:
                plt.close(fig)
            if save_path is not None:
                fig.savefig(save_path, dpi=dpi)

        return profile_values, distances, z_axis
