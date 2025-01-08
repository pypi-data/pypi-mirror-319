import h5py
import copy
import warnings
import textwrap
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import scipy
from obspy import UTCDateTime
from scipy.signal import detrend as scipy_detrend
from scipy.signal import get_window, savgol_filter, welch
from matplotlib.cm import ScalarMappable
from matplotlib.ticker import LogLocator
from matplotlib.colors import Normalize
from shakecore.setting import MAX_DATA_THRESHOLD
from shakecore.viz.utils.viz_tools import _format_time_axis, _get_ax, _get_cmap


def load_ppsd(
    filename,
    starttrace=None,
    endtrace=None,
    steptrace=1,
    freqmin=None,
    freqmax=None,
    stepfreq=1,
):
    with h5py.File(filename, "r") as f:
        group = f["ppsd"]
        starttime = UTCDateTime(group.attrs["starttime"])
        endtime = UTCDateTime(group.attrs["endtime"])
        ppsd_len = group.attrs["ppsd_len"]
        ppsd_step = group.attrs["ppsd_step"]
        method = group.attrs["method"]
        trace_num = group.attrs["trace_num"]

        # check starttrace and endtrace
        if starttrace is None:
            starttrace = 0
        if endtrace is None:
            endtrace = trace_num

        if starttrace < 0 or endtrace > trace_num:
            raise ValueError(
                "starttrace and endtrace must be within the ppsd trace range."
            )

        # check freqmin and freqmax
        f_axis_raw = group["f_axis"][:]
        df = f_axis_raw[1] - f_axis_raw[0]
        if freqmin is None:
            freqmin = f_axis_raw[0]
        if freqmax is None:
            freqmax = f_axis_raw[-1]
        i1 = int((freqmin - f_axis_raw[0]) / df)
        i2 = int((freqmax - f_axis_raw[0]) / df) + 1

        if i1 < 0 or i2 > len(f_axis_raw):
            raise ValueError(
                "freqmin and freqmax must be within the ppsd frequency range."
            )

        # load data
        data = group["data"][starttrace:endtrace:steptrace, i1:i2:stepfreq]
        f_axis = f_axis_raw[i1:i2:stepfreq]
        network = group.attrs["network"].tolist()[starttrace:endtrace:steptrace]
        station = group.attrs["station"].tolist()[starttrace:endtrace:steptrace]
        location = group.attrs["location"].tolist()[starttrace:endtrace:steptrace]
        channel = group.attrs["channel"].tolist()[starttrace:endtrace:steptrace]

        ppsd = PPSD(
            data,
            f_axis,
            network,
            station,
            location,
            channel,
            starttime,
            endtime,
            ppsd_len,
            ppsd_step,
            method,
        )

    return ppsd


def load_ppsd_trace(
    filename,
    starttime=None,
    endtime=None,
    freqmin=None,
    freqmax=None,
    stepfreq=1,
):
    with h5py.File(filename, "r") as f:
        group = f["ppsd"]
        network = group.attrs["network"]
        station = group.attrs["station"]
        location = group.attrs["location"]
        channel = group.attrs["channel"]
        ppsd_len = group.attrs["ppsd_len"]
        ppsd_step = group.attrs["ppsd_step"]
        method = group.attrs["method"]

        # check starttime and endtime
        starttime_raw = UTCDateTime(group.attrs["starttime"])
        endtime_raw = UTCDateTime(group.attrs["endtime"])
        times_raw = group["times"][:]
        for i in range(0, len(times_raw)):
            times_raw[i, 0] = UTCDateTime(times_raw[i, 0])
            times_raw[i, 1] = UTCDateTime(times_raw[i, 1])

        if starttime is None:
            starttime = starttime_raw
        if endtime is None:
            endtime = endtime_raw

        if (starttime > endtime_raw or starttime < starttime_raw) or (
            endtime < starttime_raw or endtime > endtime_raw
        ):
            raise ValueError(
                "starttime and endtime must be within the ppsd time range."
            )

        # check freqmin and freqmax
        f_axis_raw = group["f_axis"][:]
        df = f_axis_raw[1] - f_axis_raw[0]
        if freqmin is None:
            freqmin = f_axis_raw[0]
        if freqmax is None:
            freqmax = f_axis_raw[-1]
        i1 = int((freqmin - f_axis_raw[0]) / df)
        i2 = int((freqmax - f_axis_raw[0]) / df) + 1

        if i1 < 0 or i2 > len(f_axis_raw):
            raise ValueError(
                "freqmin and freqmax must be within the ppsd frequency range."
            )

        # load data
        start_index = np.argmin(np.abs(times_raw[:, 0] - starttime))
        end_index = np.argmin(np.abs(times_raw[:, 1] - endtime)) + 1
        times = times_raw[start_index:end_index]
        data = group["data"][start_index:end_index, i1:i2:stepfreq]
        f_axis = f_axis_raw[i1:i2:stepfreq]

        ppsd_temporal = PPSD_Trace(
            data,
            f_axis,
            times,
            network,
            station,
            location,
            channel,
            ppsd_len,
            ppsd_step,
            method,
        )

    return ppsd_temporal


def load_ppsd_freq(
    filename,
    starttrace=None,
    endtrace=None,
    steptrace=1,
    starttime=None,
    endtime=None,
):
    with h5py.File(filename, "r") as f:
        group = f["ppsd"]
        freq = group.attrs["freq"]
        ppsd_len = group.attrs["ppsd_len"]
        ppsd_step = group.attrs["ppsd_step"]
        method = group.attrs["method"]
        trace_num = group.attrs["trace_num"]

        # check starttrace and endtrace
        if starttrace is None:
            starttrace = 0
        if endtrace is None:
            endtrace = trace_num

        if starttrace < 0 or endtrace > trace_num:
            raise ValueError(
                "starttrace and endtrace must be within the ppsd trace range."
            )

        # check starttime and endtime
        starttime_raw = UTCDateTime(group.attrs["starttime"])
        endtime_raw = UTCDateTime(group.attrs["endtime"])
        times_raw = group["times"][:]
        for i in range(0, len(times_raw)):
            times_raw[i, 0] = UTCDateTime(times_raw[i, 0])
            times_raw[i, 1] = UTCDateTime(times_raw[i, 1])

        if starttime is None:
            starttime = starttime_raw
        if endtime is None:
            endtime = endtime_raw

        if (starttime > endtime_raw or starttime < starttime_raw) or (
            endtime < starttime_raw or endtime > endtime_raw
        ):
            raise ValueError(
                "starttime and endtime must be within the ppsd time range."
            )

        # load data
        start_index = np.argmin(np.abs(times_raw[:, 0] - starttime))
        end_index = np.argmin(np.abs(times_raw[:, 1] - endtime)) + 1
        times = times_raw[start_index:end_index]
        data = group["data"][start_index:end_index, starttrace:endtrace:steptrace]
        network = group.attrs["network"].tolist()[starttrace:endtrace:steptrace]
        station = group.attrs["station"].tolist()[starttrace:endtrace:steptrace]
        location = group.attrs["location"].tolist()[starttrace:endtrace:steptrace]
        channel = group.attrs["channel"].tolist()[starttrace:endtrace:steptrace]

        ppsd_freq = PPSD_Freq(
            data,
            times,
            freq,
            network,
            station,
            location,
            channel,
            ppsd_len,
            ppsd_step,
            method,
        )

    return ppsd_freq


def compute_ppsd(data, fs, ppsd_len, ppsd_step, method):
    """_summary_

    Args:
        data (_type_): _description_
        fs (_type_): _description_
        ppsd_len (_type_): _description_
        ppsd_step (_type_): _description_
        method (_type_): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_

    Note:
        _note_
        Do need divide nperseg, because we divide the window power before???
    """
    npts = data.shape[1]
    trace_num = data.shape[0]
    nperseg = int(ppsd_len * fs)
    noverlap = int(ppsd_step * fs)

    if method == "welch":
        f_axis, ppsd_data = welch(
            data,
            fs=fs,
            nperseg=nperseg,
            noverlap=noverlap,
            axis=1,
        )
        ppsd_data = 10 * np.log10(ppsd_data)
    elif method == "rfft":
        f_axis = scipy.fft.rfftfreq(nperseg, 1 / fs)
        scipy_detrend(data, axis=1, type="linear", overwrite_data=True)
        window = get_window("hann", nperseg)
        step = nperseg - noverlap
        win_num = (npts - noverlap) // step
        ppsd_data = np.zeros((trace_num, nperseg // 2 + 1))
        for i in range(win_num):
            npts1 = i * step
            npts2 = npts1 + nperseg
            seg = data[:, npts1:npts2]
            seg_window = seg * window
            seg_rfft = scipy.fft.rfft(seg_window, n=nperseg, axis=1)
            ppsd_data += np.abs(seg_rfft) ** 2

        ppsd_data = ppsd_data / win_num / (fs * (window**2).sum())
        ppsd_data = 10 * np.log10(ppsd_data)
    else:
        raise ValueError("method must be 'welch' or 'fft'")

    return ppsd_data, f_axis


def ppsd(
    self,
    ppsd_len,
    ppsd_step,
    starttrace=None,
    endtrace=None,
    starttime=None,
    endtime=None,
    method="welch",  # welch or rfft
):
    # check starttime and endtime
    if starttime is None:
        starttime = self.stats.starttime
    if starttime < self.stats.starttime:
        raise ValueError("starttime must be greater than or equal to stream starttime.")
    if endtime is None:
        endtime = self.stats.endtime
    if endtime > self.stats.endtime:
        raise ValueError("endtime must be less than or equal to stream endtime.")

    # check starttrace and endtrace
    if starttrace is None:
        starttrace = int(0)
    if starttrace < 0:
        raise ValueError("starttrace must be greater than or equal to 0.")
    if endtrace is None:
        endtrace = int(self.stats.trace_num)
    if endtrace > self.stats.trace_num:
        raise ValueError("endtrace must be less than or equal to stream trace_num.")

    # set times
    starttime_npts = int((starttime - self.stats.starttime) * self.stats.sampling_rate)
    endtime_npts = int((endtime - self.stats.starttime) * self.stats.sampling_rate)

    # data
    data = self.data[starttrace:endtrace, starttime_npts:endtime_npts].copy()
    network = self.stats.network[starttrace:endtrace]
    station = self.stats.station[starttrace:endtrace]
    location = self.stats.location[starttrace:endtrace]
    channel = self.stats.channel[starttrace:endtrace]

    # ppsd compute
    ppsd_data, f_axis = compute_ppsd(
        data, self.stats.sampling_rate, ppsd_len, ppsd_step, method
    )

    # generate ppsd object
    PPSD_Data = PPSD(
        ppsd_data,
        f_axis,
        network,
        station,
        location,
        channel,
        starttime,
        endtime,
        ppsd_len,
        ppsd_step,
        method,
    )

    return PPSD_Data


class PPSD(object):
    def __init__(
        self,
        data,
        f_axis,
        network=None,
        station=None,
        location=None,
        channel=None,
        starttime=UTCDateTime(0),
        endtime=UTCDateTime(0),
        ppsd_len=-1,
        ppsd_step=-1,
        method="",
    ):
        self.data = data
        self.f_axis = f_axis
        self.df = f_axis[1] - f_axis[0]
        self.starttime = starttime
        self.endtime = endtime
        self.ppsd_len = ppsd_len
        self.ppsd_step = ppsd_step
        self.method = method
        self.trace_num = data.shape[0]
        self.freq_npts = data.shape[1]

        if network is None:
            network = [""] * self.trace_num

        if station is None:
            station = [""] * self.trace_num

        if location is None:
            location = [""] * self.trace_num

        if channel is None:
            channel = [""] * self.trace_num

        self.network = network
        self.station = station
        self.location = location
        self.channel = channel

    def __str__(self):
        stats = (
            "* Stats:\n"
            f"      starttime: {str(self.starttime)}\n"
            f"        endtime: {str(self.endtime)}\n"
            f"       ppsd_len: {self.ppsd_len}\n"
            f"      ppsd_step: {self.ppsd_step}\n"
            f"         method: {self.method}\n"
            f"             df: {self.df}\n"
        )
        data = (
            "* Data:\n"
            f"       shape: {self.data.shape} || (trace_num, freq_npts)\n"
            f"       dtype: {self.data.dtype}\n"
            f"{textwrap.indent(np.array2string(self.data, threshold=MAX_DATA_THRESHOLD), '      ')}"
        )
        info = "\n".join([stats, data])
        return info

    def __repr__(self):
        return str(self)

    def copy(self):
        return copy.deepcopy(self)

    def resample(self, factor, copy=True):
        if copy:
            data = self.data[:, ::factor]
            f_axis = self.f_axis[::factor]
            return PPSD(
                data,
                f_axis,
                self.network,
                self.station,
                self.location,
                self.channel,
                self.starttime,
                self.endtime,
                self.ppsd_len,
                self.ppsd_step,
                self.method,
            )
        else:
            self.data = self.data[:, ::factor]
            self.f_axis = self.f_axis[::factor]

    def save(self, filename):
        with h5py.File(filename, "w") as f:
            group = f.create_group("ppsd")
            group.create_dataset("data", data=self.data)
            group.create_dataset("f_axis", data=self.f_axis)
            group.attrs["network"] = self.network
            group.attrs["station"] = self.station
            group.attrs["location"] = self.location
            group.attrs["channel"] = self.channel
            group.attrs["starttime"] = str(self.starttime)
            group.attrs["endtime"] = str(self.endtime)
            group.attrs["ppsd_len"] = self.ppsd_len
            group.attrs["ppsd_step"] = self.ppsd_step
            group.attrs["method"] = self.method
            group.attrs["trace_num"] = self.trace_num
            group.attrs["freq_npts"] = self.freq_npts

    def plot(
        self,
        starttrace=0,
        endtrace=1,
        freqmin=None,
        freqmax=None,
        resample_factor=None,
        freq_log=True,
        filter=False,
        window_length=201,
        polyorder=2,
        mode="mesh",  # mesh or line
        xbins=50,
        ybins=50,
        meshline=True,
        linecolor="gray",
        linewidth=1,
        linestyle="-",
        linealpha=0.8,
        clip=[None, None],
        ax=None,
        figsize=(10, 5),
        cmap="CMRmap_r",
        show_legend=True,
        show=True,
        save_path=None,
        dpi=100,
    ):
        # check starttrace and endtrace
        if starttrace < 0:
            raise ValueError("starttrace must be greater than or equal to 0.")
        if endtrace > self.trace_num:
            raise ValueError("endtrace must be less than or equal to stream trace_num.")

        # check freq_range
        if freqmin is None:
            freqmin = self.f_axis[1]  # skip 0 Hz to avoid log(0)
        if freqmax is None:
            freqmax = self.f_axis[-1]
        n1 = int((freqmin - self.f_axis[0]) / self.df)
        n2 = int((freqmax - self.f_axis[0]) / self.df)
        f_axis = self.f_axis[n1:n2]

        # data & smooth
        data = self.data[starttrace:endtrace, n1:n2].copy()
        data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
        if filter:
            data = savgol_filter(data, window_length, polyorder, axis=1)

        # resample
        if resample_factor is not None:
            data = data[:, ::resample_factor]
            f_axis = f_axis[::resample_factor]

        # clip
        if clip[0] is None:
            clip[0] = np.nanmin(data)
        if clip[1] is None:
            clip[1] = np.nanmax(data)

        # plot
        ax = _get_ax(ax, figsize=figsize)
        cmap = _get_cmap(cmap)
        if mode == "line":
            if type(linecolor) == str:
                colors = [linecolor]
            else:
                colors = linecolor
            color_num = len(colors)
            for i in range(0, data.shape[0]):
                # skip all zero trace
                if not data[i].all() == 0:
                    ax.plot(
                        f_axis,
                        data[i],
                        color=colors[i % color_num],
                        linewidth=linewidth,
                        linestyle=linestyle,
                        alpha=linealpha,
                        label=f"trace:{i+starttrace}",
                    )
        elif mode == "mesh":
            # remove all 0 rows
            data = data[~np.all(data == 0.0, axis=1)]
            # mesh grid
            x_edges = np.linspace(f_axis[0], f_axis[-1], xbins)
            y_edges = np.linspace(data.min(), data.max(), ybins)
            X, Y = np.meshgrid(x_edges[:-1], y_edges[:-1])
            density = np.zeros(X.shape)
            for curve in data:
                H, _, _ = np.histogram2d(f_axis, curve, bins=(x_edges, y_edges))
                density += H.T
            density /= np.max(density)
            im = ax.pcolormesh(X, Y, density, cmap=cmap, shading="auto")
            # mean line
            if meshline:
                mean = np.mean(data, axis=0)
                ax.plot(
                    f_axis,
                    mean,
                    color=linecolor,
                    linewidth=linewidth,
                    linestyle=linestyle,
                    alpha=linealpha,
                )
        else:
            raise ValueError("mode must be 'mesh' or 'line'")

        # format
        fig = ax.figure
        if freq_log:
            ax.set_xscale("log")
        ax.set_xlim([freqmin, freqmax])
        ax.set_ylim(clip)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("PSD (dB)")

        if mode == "mesh":
            cbar = fig.colorbar(im, ax=ax, extend="both")
            cbar.set_label("Probability")
        if mode == "line" and show_legend:
            ax.legend(loc="upper right", fontsize=8, shadow=False)

        if show:
            plt.show()
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return ax

    def plot_spatial(
        self,
        starttrace=0,
        endtrace=1,
        freqmin=None,
        freqmax=None,
        resample_factor=None,
        freq_log=True,
        filter=False,
        window_length=201,
        polyorder=2,
        freq_lines=[],  # list of frequency
        reverse_freq_lines=False,
        trace_lines=[],  # list of trace
        reverse_trace_lines=False,
        linecolor="black",
        linewidth=1,
        linestyle="-",
        linealpha=0.8,
        linescale=0.2,
        trace_axis="x",
        trace_ticks=5,
        invert_x=False,
        invert_y=False,
        clip=[None, None],
        ax=None,
        figsize=(10, 6),
        cmap="viridis",
        show=True,
        save_path=None,
        dpi=100,
    ):
        # check starttrace and endtrace
        if starttrace < 0:
            raise ValueError("starttrace must be greater than or equal to 0.")
        if endtrace > self.trace_num:
            raise ValueError("endtrace must be less than or equal to stream trace_num.")
        trace_num = endtrace - starttrace

        # check freq_range
        if freqmin is None:
            freqmin = self.f_axis[1]
        if freqmax is None:
            freqmax = self.f_axis[-1]
        n1 = int((freqmin - self.f_axis[0]) / self.df)
        n2 = int((freqmax - self.f_axis[0]) / self.df)
        f_axis = self.f_axis[n1:n2]

        # data & smooth
        data = self.data[starttrace:endtrace, n1:n2].copy()
        data[np.isinf(data)] = np.nan
        if filter:
            if np.nan in data:
                warnings.warn(
                    "Data contains NaN values, NaN values will be replaced with 0.",
                    UserWarning,
                )
                data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
            data = savgol_filter(data, window_length, polyorder, axis=1)

        # resample
        if resample_factor is not None:
            data = data[:, ::resample_factor]
            f_axis = f_axis[::resample_factor]

        # data freq lines
        if len(freq_lines) != 0:
            freq_lines_data = np.full((len(freq_lines), trace_num), np.nan)
            for i in range(0, len(freq_lines)):
                # find freq band from f_axis
                freq_min_index = np.argmin(np.abs(f_axis - freq_lines[i][0]))
                freq_max_index = np.argmin(np.abs(f_axis - freq_lines[i][1]))
                freq_lines_data[i, :] = np.nanmean(
                    data[:, freq_min_index:freq_max_index], axis=1
                )
            freq_lines_data += -np.nanmin(freq_lines_data)  # shift to positive from dB

        # data trace lines
        if len(trace_lines) != 0:
            trace_lines_data = np.full((len(trace_lines), len(f_axis)), np.nan)
            for i in range(0, len(trace_lines)):
                # find trace band from data
                m1 = trace_lines[i][0]
                m2 = trace_lines[i][1]
                trace_lines_data[i, :] = np.nanmean(data[m1:m2, :], axis=0)
            trace_lines_data += -np.nanmin(trace_lines_data)  # shift to positive

        # clip
        if clip[0] is None:
            clip[0] = np.nanmin(data)
        if clip[1] is None:
            clip[1] = np.nanmax(data)

        # plot
        ax = _get_ax(ax, figsize=figsize)
        cmap = _get_cmap(cmap)
        if trace_axis == "x":
            im = ax.imshow(
                data.T,
                extent=[starttrace, endtrace, freqmin, freqmax],
                aspect="auto",
                cmap=cmap,
                origin="lower",
            )
        elif trace_axis == "y":
            im = ax.imshow(
                data,
                extent=[freqmin, freqmax, starttrace, endtrace],
                aspect="auto",
                cmap=cmap,
                origin="lower",
            )
        else:
            raise ValueError("time_axis must be 'x' or 'y'")

        # plot freq lines
        if reverse_freq_lines:
            c_freq = -1
        else:
            c_freq = 1
        if len(freq_lines) != 0:
            traces_axis = np.linspace(starttrace, endtrace - 1, num=trace_num)
            for i in range(0, len(freq_lines)):
                y_shift = (freq_lines[i][1] + freq_lines[i][0]) / 2
                line_data = np.abs(freq_lines_data[i, :]) - np.nanmin(
                    np.abs(freq_lines_data[i, :])
                )
                if np.nanmax(line_data) == 0:
                    line_data = np.full(line_data.shape, y_shift)
                else:
                    line_data = (
                        c_freq * line_data / np.nanmax(line_data) * linescale
                        - linescale / 2
                        + y_shift
                    )
                if trace_axis == "x":
                    ax.plot(
                        traces_axis,
                        line_data,
                        color=linecolor,
                        linewidth=linewidth,
                        linestyle=linestyle,
                        alpha=linealpha,
                    )
                elif trace_axis == "y":
                    ax.plot(
                        line_data,
                        traces_axis,
                        color=linecolor,
                        linewidth=linewidth,
                        linestyle=linestyle,
                        alpha=linealpha,
                    )

        # plot trace lines
        if reverse_trace_lines:
            c_trace = -1
        else:
            c_trace = 1
        if len(trace_lines) != 0:
            for i in range(0, len(trace_lines)):
                x_shift = (trace_lines[i][1] + trace_lines[i][0]) / 2
                line_data = np.abs(trace_lines_data[i, :]) - np.nanmin(
                    np.abs(trace_lines_data[i, :])
                )
                if np.nanmax(line_data) == 0:
                    line_data = np.full(line_data.shape, x_shift)
                else:
                    line_data = (
                        c_trace * line_data / np.nanmax(line_data) * linescale
                        - linescale / 2
                        + x_shift
                    )
                if trace_axis == "x":
                    ax.plot(
                        line_data,
                        f_axis,
                        color=linecolor,
                        linewidth=linewidth,
                        linestyle=linestyle,
                        alpha=linealpha,
                    )
                elif trace_axis == "y":
                    ax.plot(
                        f_axis,
                        line_data,
                        color=linecolor,
                        linewidth=linewidth,
                        linestyle=linestyle,
                        alpha=linealpha,
                    )

        # clip
        im.set_clim(clip)

        # format axis
        if trace_ticks > (endtrace - starttrace - 1):
            trace_ticks = round(endtrace - starttrace - 1)
        ticks = np.linspace(starttrace, endtrace - 1, num=trace_ticks)
        labels = np.round(
            np.linspace(starttrace, endtrace - 1, num=trace_ticks)
        ).astype(int)
        if trace_axis == "x":
            if freq_log:
                ax.set_yscale("log")
            ax.set_xlim([starttrace, endtrace])
            ax.set_ylim([freqmin, freqmax])
            ax.set_xticks(ticks)
            ax.set_xticklabels(labels)
            ax.set_xlabel("Trace")
            ax.set_ylabel("Frequency (Hz)")
        elif trace_axis == "y":
            if freq_log:
                ax.set_xscale("log")
            ax.set_xlim([freqmin, freqmax])
            ax.set_ylim([starttrace, endtrace])
            ax.set_yticks(ticks)
            ax.set_yticklabels(labels)
            ax.set_ylabel("Trace")
            ax.set_xlabel("Frequency (Hz)")
        else:
            raise ValueError("trace_axis must be 'x' or 'y'")

        # format figure
        fig = ax.figure
        cbar = fig.colorbar(im, ax=ax, extend="both")
        cbar.set_label("PSD (dB)")
        if invert_x:
            ax.invert_xaxis()
        if invert_y:
            ax.invert_yaxis()
        if show:
            plt.show()
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return ax


class PPSD_Trace(object):
    def __init__(
        self,
        data,
        f_axis,
        times,
        network="",
        station="",
        location="",
        channel="",
        ppsd_len=-1,
        ppsd_step=-1,
        method="",
    ):
        self.network = network
        self.station = station
        self.location = location
        self.channel = channel
        self.ppsd_len = ppsd_len
        self.ppsd_step = ppsd_step
        self.method = method
        self.time_num = data.shape[0]
        self.freq_npts = data.shape[1]

        sorted_indices = np.argsort(times[:, 0])
        self.data = data[sorted_indices]
        self.times = times[sorted_indices]
        self.f_axis = f_axis
        self.starttime = times[0, 0]
        self.endtime = times[-1, 1]
        self.df = f_axis[1] - f_axis[0]

    def __str__(self):
        stats = (
            "* Stats:\n"
            f"      starttime: {str(self.starttime)}\n"
            f"        endtime: {str(self.endtime)}\n"
            f"       ppsd_len: {self.ppsd_len}\n"
            f"      ppsd_step: {self.ppsd_step}\n"
            f"         method: {self.method}\n"
            f"             df: {self.df}\n"
        )
        data = (
            "* Data:\n"
            f"       shape: {self.data.shape} || (time_num, freq_npts)\n"
            f"       dtype: {self.data.dtype}\n"
            f"{textwrap.indent(np.array2string(self.data, threshold=MAX_DATA_THRESHOLD), '      ')}"
        )
        info = "\n".join([stats, data])
        return info

    def __repr__(self):
        return str(self)

    def copy(self):
        return copy.deepcopy(self)

    def resample(self, factor, copy=True):
        if copy:
            data = self.data[:, ::factor]
            f_axis = self.f_axis[::factor]
            return PPSD_Trace(
                data,
                f_axis,
                self.times,
                self.network,
                self.station,
                self.location,
                self.channel,
                self.ppsd_len,
                self.ppsd_step,
                self.method,
            )
        else:
            self.data = self.data[:, ::factor]
            self.f_axis = self.f_axis[::factor]

    def save(self, filename):
        with h5py.File(filename, "w") as f:
            group = f.create_group("ppsd")
            group.create_dataset("data", data=self.data)
            group.create_dataset("f_axis", data=self.f_axis)
            times = np.empty(self.times.shape, dtype=object)
            for i in range(0, self.time_num):
                times[i] = [str(self.times[i, 0]), str(self.times[i, 1])]
            group.create_dataset("times", data=times)
            group.attrs["network"] = self.network
            group.attrs["station"] = self.station
            group.attrs["location"] = self.location
            group.attrs["channel"] = self.channel
            group.attrs["starttime"] = str(self.starttime)
            group.attrs["endtime"] = str(self.endtime)
            group.attrs["ppsd_len"] = self.ppsd_len
            group.attrs["ppsd_step"] = self.ppsd_step
            group.attrs["method"] = self.method
            group.attrs["time_num"] = self.time_num
            group.attrs["freq_npts"] = self.freq_npts

    def plot(
        self,
        starttime=None,
        endtime=None,
        freqmin=None,
        freqmax=None,
        resample_factor=None,
        freq_lines=[],  # list of frequency
        reverse_freq_lines=False,
        freq_log=True,
        linecolor="black",
        linewidth=1,
        linestyle="-",
        linealpha=0.8,
        linescale=0.2,
        filter=False,
        window_length=201,
        polyorder=2,
        time_minticks=5,
        time_maxticks=None,
        timetick_rotation=0,
        timetick_labelsize=10,
        ax=None,
        cmap="viridis",
        clip=[None, None],
        figsize=(10, 6),
        show=True,
        save_path=None,
        dpi=100,
    ):
        # check freq_range
        if freqmin is None:
            freqmin = self.f_axis[1]
        if freqmax is None:
            freqmax = self.f_axis[-1]
        n1 = int((freqmin - self.f_axis[0]) / self.df)
        n2 = int((freqmax - self.f_axis[0]) / self.df)
        f_axis = self.f_axis[n1:n2]

        # data & smooth, average data from all ppsd
        if starttime is None:
            starttime = self.starttime
        if endtime is None:
            endtime = self.endtime
        total_seconds = endtime - starttime
        min_interval = np.min(self.times[:, 1] - self.times[:, 0])
        time_bins = int(total_seconds / min_interval)
        data = np.full((time_bins, len(f_axis)), np.nan)
        for i in range(0, self.time_num):
            if self.times[i, 0] >= starttime and self.times[i, 1] < endtime:
                dd = self.data[i, n1:n2].copy()
                dd[np.isinf(dd)] = np.nan
                index1 = int((self.times[i, 0] - starttime) / min_interval)
                index2 = int((self.times[i, 1] - starttime) / min_interval)
                data[index1:index2, :] = dd
        if filter:
            if np.nan in data:
                warnings.warn(
                    "Data contains NaN values, NaN values will be replaced with 0.",
                    UserWarning,
                )
                data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
            data = savgol_filter(data, window_length, polyorder, axis=1)

        # resample
        if resample_factor is not None:
            data = data[:, ::resample_factor]
            f_axis = f_axis[::resample_factor]

        # data freq lines
        if len(freq_lines) != 0:
            freq_lines_data = np.full((len(freq_lines), time_bins), np.nan)
            for i in range(0, len(freq_lines)):
                # find freq band from f_axis
                freq_min_index = np.argmin(np.abs(f_axis - freq_lines[i][0]))
                freq_max_index = np.argmin(np.abs(f_axis - freq_lines[i][1]))
                freq_lines_data[i, :] = np.nanmean(
                    data[:, freq_min_index:freq_max_index], axis=1
                )
            freq_lines_data += -np.nanmin(freq_lines_data)  # shift to positive from dB

        # clip
        if clip[0] is None:
            clip[0] = np.nanmin(data)
        if clip[1] is None:
            clip[1] = np.nanmax(data)

        # plot data
        ax = _get_ax(ax, figsize=figsize)
        cmap = _get_cmap(cmap)
        im = ax.imshow(
            data.T,
            extent=[starttime.datetime, endtime.datetime, freqmin, freqmax],
            aspect="auto",
            cmap=cmap,
            origin="lower",
        )

        # plot freq lines
        if reverse_freq_lines:
            c_freq = -1
        else:
            c_freq = 1
        if len(freq_lines) != 0:
            times_axis = np.empty(time_bins, dtype=object)
            for i in range(0, time_bins):
                times_axis[i] = (
                    starttime + i * min_interval + 0.5 * min_interval
                ).datetime
            for i in range(0, len(freq_lines)):
                y_shift = (freq_lines[i][1] + freq_lines[i][0]) / 2
                line_data = np.abs(freq_lines_data[i, :]) - np.nanmin(
                    np.abs(freq_lines_data[i, :])
                )
                if np.nanmax(line_data) == 0:
                    line_data = np.full(line_data.shape, y_shift)
                else:
                    line_data = (
                        c_freq * line_data / np.nanmax(line_data) * linescale
                        - linescale / 2
                        + y_shift
                    )
                ax.plot(
                    times_axis,
                    line_data,
                    color=linecolor,
                    linewidth=linewidth,
                    linestyle=linestyle,
                    alpha=linealpha,
                )

        # clip
        im.set_clim(clip)

        # format axis
        _format_time_axis(
            ax,
            axis="x",
            tick_rotation=timetick_rotation,
            minticks=time_minticks,
            maxticks=time_maxticks,
            labelsize=timetick_labelsize,
        )
        if freq_log:
            ax.set_yscale("log")
        ax.set_xlim([starttime.datetime, endtime.datetime])
        ax.set_ylim([freqmin, freqmax])
        ax.set_ylabel("Frequency (Hz)")

        # format figure
        fig = ax.figure
        cbar = fig.colorbar(im, ax=ax, extend="both")
        cbar.set_label("PSD (dB)")
        if show:
            plt.show()
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return ax


class PPSD_Freq(object):
    def __init__(
        self,
        data,
        times,
        freq=[-1, -1],
        network=None,
        station=None,
        location=None,
        channel=None,
        ppsd_len=-1,
        ppsd_step=-1,
        method="",
    ):
        self.freq = freq
        self.ppsd_len = ppsd_len
        self.ppsd_step = ppsd_step
        self.method = method
        self.time_num = data.shape[0]
        self.trace_num = data.shape[1]

        sorted_indices = np.argsort(times[:, 0])
        self.data = data[sorted_indices]
        self.times = times[sorted_indices]
        self.starttime = times[0, 0]
        self.endtime = times[-1, 1]

        if network is None:
            network = [""] * self.trace_num

        if station is None:
            station = [""] * self.trace_num

        if location is None:
            location = [""] * self.trace_num

        if channel is None:
            channel = [""] * self.trace_num

        self.network = network
        self.station = station
        self.location = location
        self.channel = channel

    def __str__(self):
        stats = (
            "* Stats:\n"
            f"      starttime: {str(self.starttime)}\n"
            f"        endtime: {str(self.endtime)}\n"
            f"       ppsd_len: {self.ppsd_len}\n"
            f"      ppsd_step: {self.ppsd_step}\n"
            f"         method: {self.method}\n"
            f"           freq: {self.freq}\n"
        )
        data = (
            "* Data:\n"
            f"       shape: {self.data.shape} || (time_num, trace_num)\n"
            f"       dtype: {self.data.dtype}\n"
            f"{textwrap.indent(np.array2string(self.data, threshold=MAX_DATA_THRESHOLD), '      ')}"
        )
        info = "\n".join([stats, data])
        return info

    def __repr__(self):
        return str(self)

    def copy(self):
        return copy.deepcopy(self)

    def save(self, filename):
        with h5py.File(filename, "w") as f:
            group = f.create_group("ppsd")
            group.create_dataset("data", data=self.data)
            times = np.empty(self.times.shape, dtype=object)
            for i in range(0, self.time_num):
                times[i] = [str(self.times[i, 0]), str(self.times[i, 1])]
            group.create_dataset("times", data=times)
            group.attrs["freq"] = self.freq
            group.attrs["network"] = self.network
            group.attrs["station"] = self.station
            group.attrs["location"] = self.location
            group.attrs["channel"] = self.channel
            group.attrs["starttime"] = str(self.starttime)
            group.attrs["endtime"] = str(self.endtime)
            group.attrs["ppsd_len"] = self.ppsd_len
            group.attrs["ppsd_step"] = self.ppsd_step
            group.attrs["method"] = self.method
            group.attrs["time_num"] = self.time_num
            group.attrs["trace_num"] = self.trace_num

    def plot(
        self,
        starttrace=None,
        endtrace=None,
        starttime=None,
        endtime=None,
        trace_lines=[],  # list of frequency
        reverse_trace_lines=False,
        linecolor="black",
        linewidth=1,
        linestyle="-",
        linealpha=0.8,
        linescale=0.2,
        filter=False,
        window_length=201,
        polyorder=2,
        time_minticks=5,
        time_maxticks=None,
        timetick_rotation=0,
        timetick_labelsize=10,
        ax=None,
        cmap="viridis",
        clip=[None, None],
        figsize=(10, 6),
        show=True,
        save_path=None,
        dpi=100,
    ):
        # check starttrace and endtrace
        if starttrace is None:
            starttrace = 0
        if endtrace is None:
            endtrace = self.trace_num
        trace_num = endtrace - starttrace

        # check starttime and endtime
        if starttime is None:
            starttime = self.starttime
        if endtime is None:
            endtime = self.endtime

        # data & smooth, average data from all ppsd
        total_seconds = endtime - starttime
        min_interval = np.min(self.times[:, 1] - self.times[:, 0])
        time_bins = int(total_seconds / min_interval)
        data = np.full((time_bins, trace_num), np.nan)
        for i in range(0, self.time_num):
            if self.times[i, 0] >= starttime and self.times[i, 1] < endtime:
                dd = self.data[i, starttrace:endtrace].copy()
                dd[np.isinf(dd)] = np.nan
                index1 = int((self.times[i, 0] - starttime) / min_interval)
                index2 = int((self.times[i, 1] - starttime) / min_interval)
                data[index1:index2, :] = dd
        if filter:
            if np.nan in data:
                warnings.warn(
                    "Data contains NaN values, NaN values will be replaced with 0.",
                    UserWarning,
                )
                data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
            data = savgol_filter(data, window_length, polyorder, axis=1)

        # data trace lines
        if len(trace_lines) != 0:
            trace_lines_data = np.full((len(trace_lines), time_bins), np.nan)
            for i in range(0, len(trace_lines)):
                n1 = trace_lines[i][0] - starttrace
                n2 = trace_lines[i][1] - starttrace
                trace_lines_data[i, :] = np.nanmean(data[:, n1:n2], axis=1)
            trace_lines_data += -np.nanmin(trace_lines_data)  # shift to positive

        # clip
        if clip[0] is None:
            clip[0] = np.nanmin(data)
        if clip[1] is None:
            clip[1] = np.nanmax(data)

        # plot data
        ax = _get_ax(ax, figsize=figsize)
        cmap = _get_cmap(cmap)
        im = ax.imshow(
            data.T,
            extent=[starttime.datetime, endtime.datetime, starttrace, endtrace],
            aspect="auto",
            cmap=cmap,
            origin="lower",
        )

        # plot trace lines
        if reverse_trace_lines:
            c_trace = -1
        else:
            c_trace = 1
        if len(trace_lines) != 0:
            times_axis = np.empty(time_bins, dtype=object)
            for i in range(0, time_bins):
                times_axis[i] = (
                    starttime + i * min_interval + 0.5 * min_interval
                ).datetime
            for i in range(0, len(trace_lines)):
                y_shift = (trace_lines[i][1] + trace_lines[i][0]) / 2
                line_data = np.abs(trace_lines_data[i, :]) - np.nanmin(
                    np.abs(trace_lines_data[i, :])
                )
                if np.nanmax(line_data) == 0:
                    line_data = np.full(line_data.shape, y_shift)
                else:
                    line_data = (
                        c_trace * line_data / np.nanmax(line_data) * linescale
                        - linescale / 2
                        + y_shift
                    )
                ax.plot(
                    times_axis,
                    line_data,
                    color=linecolor,
                    linewidth=linewidth,
                    linestyle=linestyle,
                    alpha=linealpha,
                )

        # clip
        im.set_clim(clip)

        # format axis
        _format_time_axis(
            ax,
            axis="x",
            tick_rotation=timetick_rotation,
            minticks=time_minticks,
            maxticks=time_maxticks,
            labelsize=timetick_labelsize,
        )
        ax.set_xlim([starttime.datetime, endtime.datetime])
        ax.set_ylim([starttrace, endtrace])
        ax.set_ylabel("Trace #")
        ax.invert_yaxis()

        # format figure
        fig = ax.figure
        cbar = fig.colorbar(im, ax=ax, extend="both")
        cbar.set_label("PSD (dB)")
        if show:
            plt.show()
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return ax


def plot3d_ppsd(
    ppsd,
    ppsd_freq,
    ppsd_trace,
    starttrace,
    endtrace,
    freqmin,
    freqmax,
    starttime,
    endtime,
    mode="1",
    freq_log=False,
    freq_ticks=[],
    rcount=100,
    ccount=100,
    time_minticks=5,
    time_maxticks=None,
    timetick_rotation=0,
    timetick_pad=0,
    timetick_labelsize=10,
    ax=None,
    box_aspect=[1, 1, 1],
    box_aspect_zoom=0.85,
    view_init_elev=30,
    view_init_azim=30,
    cmap="viridis",
    clip=[None, None],
    colorbar_shrink=0.5,
    colorbar_pad=0.1,
    figsize=(10, 6),
    show=True,
    save_path=None,
    dpi=100,
):
    # check
    # if ppsd.df != ppsd_trace.df:
    #     raise ValueError("PPSD.df must be equal to PPSD_Trace.df.")

    # x_axis
    dx = 1
    x_axis = np.arange(starttrace, endtrace, dx)

    # f_axis
    df = ppsd.df
    f_axis_raw = np.arange(freqmin, freqmax, df)
    if freq_log:
        f_axis = np.log10(f_axis_raw)
    else:
        f_axis = f_axis_raw

    # t_axis
    dt_sec = np.min(ppsd_freq.times[:, 1] - ppsd_freq.times[:, 0])
    t_axis = mdates.date2num(np.arange(starttime, endtime, dt_sec))
    dt = t_axis[1] - t_axis[0]

    # xf_slice
    s1 = starttrace
    s2 = starttrace + len(x_axis)
    n1 = np.argmin(np.abs(ppsd.f_axis - freqmin))
    n2 = n1 + len(f_axis)
    xf_slice = ppsd.data[s1:s2, n1:n2]

    # xt_slice
    xt_slice = np.full((len(x_axis), len(t_axis)), np.nan)
    for i in range(0, ppsd_freq.time_num):
        if ppsd_freq.times[i, 0] >= starttime and ppsd_freq.times[i, 1] <= endtime:
            dd = ppsd_freq.data[i, s1:s2].copy()
            dd[np.isinf(dd)] = np.nan
            index1 = int((ppsd_freq.times[i, 0] - starttime) / dt_sec)
            index2 = int((ppsd_freq.times[i, 1] - starttime) / dt_sec)
            xt_slice[:, index1:index2] = dd[:, np.newaxis]

    # tf_slice
    tf_slice = np.full((len(t_axis), len(f_axis)), np.nan)
    for i in range(0, ppsd_trace.time_num):
        if ppsd_trace.times[i, 0] >= starttime and ppsd_trace.times[i, 1] <= endtime:
            dd = ppsd_trace.data[i, n1:n2].copy()
            dd[np.isinf(dd)] = np.nan
            index1 = int((ppsd_trace.times[i, 0] - starttime) / dt_sec)
            index2 = int((ppsd_trace.times[i, 1] - starttime) / dt_sec)
            tf_slice[index1:index2, :] = dd

    # clip
    if clip[0] is None:
        clip[0] = np.min(
            [np.nanmin(xf_slice), np.nanmin(xt_slice), np.nanmin(tf_slice)]
        )
    if clip[1] is None:
        clip[1] = np.max(
            [np.nanmax(xf_slice), np.nanmax(xt_slice), np.nanmax(tf_slice)]
        )

    # plot
    ax = _get_ax(ax, figsize=figsize, subplot_kw={"projection": "3d"})
    # cmap = _get_cmap(cmap)
    cmap_change = plt.colormaps[cmap]
    norm = Normalize(vmin=clip[0], vmax=clip[1])

    if mode == "1":
        X, F = np.meshgrid(x_axis, f_axis)
        ax.plot_surface(
            F,
            np.ones_like(X) * t_axis[-1],
            X,
            facecolors=cmap_change(norm(xf_slice.T)),
            rcount=rcount,
            ccount=ccount,
            # rstride=1, cstride=1,
            antialiased=False,
            shade=False,
        )

        T, F = np.meshgrid(t_axis, f_axis)
        ax.plot_surface(
            F,
            T,
            np.ones_like(F) * x_axis[0],
            facecolors=cmap_change(norm(tf_slice.T)),
            rcount=rcount,
            ccount=ccount,
            # rstride=1, cstride=1,
            antialiased=False,
            shade=False,
        )

        X, T = np.meshgrid(x_axis, t_axis)
        ax.plot_surface(
            np.ones_like(X) * f_axis[0],
            T,
            X,
            facecolors=cmap_change(norm(xt_slice.T)),
            rcount=rcount,
            ccount=ccount,
            # rstride=1, cstride=1,
            antialiased=False,
            shade=False,
        )

        _format_time_axis(
            ax,
            axis="y",
            minticks=time_minticks,
            maxticks=time_maxticks,
            tick_rotation=timetick_rotation,
            labelsize=timetick_labelsize,
            pad=timetick_pad,
        )

        if freq_log:
            if len(freq_ticks) != 0:
                log_labels = []
                for tick in freq_ticks:
                    exponent = int(np.floor(np.log10(tick)))
                    base = tick / (10**exponent)
                    if base == 1:  #  10^n
                        label = r"$10^{{{}}}$".format(exponent)
                    else:  #  a × 10^n
                        label = r"${}\times10^{{{}}}$".format(int(base), exponent)
                    log_labels.append(label)
                ax.xaxis.set_major_locator(
                    LogLocator(base=10.0, subs=None, numticks=10)
                )
                ax.xaxis.set_minor_locator(
                    LogLocator(base=10.0, subs=np.arange(1.0, 10.0, 1.0), numticks=50)
                )
                ax.set_xticks(np.log10(freq_ticks))
                ax.set_xticklabels(log_labels)
            else:
                ax.xaxis._set_scale("log")
        else:
            if len(freq_ticks) != 0:
                ax.set_xticks(freq_ticks)
                ax.set_xticklabels(freq_ticks)

        ax.set_xlim(f_axis[0], f_axis[-1])
        ax.set_zlim(x_axis[0], x_axis[-1])
        ax.set_ylim(t_axis[0], t_axis[-1])
        # ax.zaxis.set_major_locator(MaxNLocator(nbins=5))
        ax.set_xlabel("Frequency (Hz)")
        ax.set_zlabel("Trace #")
        ax.invert_xaxis()
        ax.invert_zaxis()
    elif mode == "2":
        X, F = np.meshgrid(x_axis, f_axis)
        ax.plot_surface(
            X,
            np.ones_like(X) * t_axis[-1],
            F,
            facecolors=cmap_change(norm(xf_slice.T)),
            rcount=rcount,
            ccount=ccount,
            # rstride=1, cstride=1,
            antialiased=False,
            shade=False,
        )

        T, F = np.meshgrid(t_axis, f_axis)
        ax.plot_surface(
            np.ones_like(F) * x_axis[0],
            T,
            F,
            facecolors=cmap_change(norm(tf_slice.T)),
            rcount=rcount,
            ccount=ccount,
            # rstride=1, cstride=1,
            antialiased=False,
            shade=False,
        )

        X, T = np.meshgrid(x_axis, t_axis)
        ax.plot_surface(
            X,
            T,
            np.ones_like(X) * f_axis[-1],
            facecolors=cmap_change(norm(xt_slice.T)),
            rcount=rcount,
            ccount=ccount,
            # rstride=1, cstride=1,
            antialiased=False,
            shade=False,
        )

        _format_time_axis(
            ax,
            axis="y",
            minticks=time_minticks,
            maxticks=time_maxticks,
            tick_rotation=timetick_rotation,
            labelsize=timetick_labelsize,
            pad=timetick_pad,
        )

        if freq_log:
            if len(freq_ticks) != 0:
                log_labels = []
                for tick in freq_ticks:
                    exponent = int(np.floor(np.log10(tick)))
                    base = tick / (10**exponent)
                    if base == 1:  #  10^n
                        label = r"$10^{{{}}}$".format(exponent)
                    else:  #  a × 10^n
                        label = r"${}\times10^{{{}}}$".format(int(base), exponent)
                    log_labels.append(label)
                ax.zaxis.set_major_locator(
                    LogLocator(base=10.0, subs=None, numticks=10)
                )
                ax.zaxis.set_minor_locator(
                    LogLocator(base=10.0, subs=np.arange(1.0, 10.0, 1.0), numticks=50)
                )
                ax.set_zticks(np.log10(freq_ticks))
                ax.set_zticklabels(log_labels)
            else:
                ax.xaxis._set_scale("log")
        else:
            if len(freq_ticks) != 0:
                ax.set_zticks(freq_ticks)
                # ax.set_zticklabels(freq_ticks)

        ax.set_xlim(x_axis[0], x_axis[-1])
        ax.set_ylim(t_axis[0], t_axis[-1])
        ax.set_zlim(f_axis[0], f_axis[-1])
        ax.set_zlabel("Frequency (Hz)")
        ax.set_xlabel("Trace #")
        ax.invert_xaxis()
    else:
        raise ValueError("mode must be '1' or '2'.")

    # format figure
    ax.set_box_aspect(box_aspect, zoom=box_aspect_zoom)
    ax.view_init(elev=view_init_elev, azim=view_init_azim)
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.xaxis._axinfo["grid"]["color"] = (1, 1, 1, 0)
    ax.yaxis._axinfo["grid"]["color"] = (1, 1, 1, 0)
    ax.zaxis._axinfo["grid"]["color"] = (1, 1, 1, 0)

    # format figure
    fig = ax.figure
    sm = ScalarMappable(cmap=cmap, norm=norm)
    plt.colorbar(sm, ax=ax, label="PSD (dB)", shrink=colorbar_shrink, pad=colorbar_pad)
    if show:
        plt.show()
    if save_path is not None:
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
    else:
        return ax
