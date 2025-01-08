import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import rfft, rfftfreq

from .utils.viz_tools import _format_freq_axis, _format_trace_axis, _get_ax


def fwaterfall(
    self,
    freqmin=None,
    freqmax=None,
    starttime=None,
    endtime=None,
    starttrace=None,
    endtrace=None,
    norm_method="stream",  # trace or stream
    freq_axis="x",
    invert_x=False,
    invert_y=False,
    freq_ticks=5,
    freqtick_rotation=0,
    freqtick_labelsize=10,
    trace_ticks=5,
    tracetick_rotation=0,
    tracetick_labelsize=10,
    trace_label="trace",  # trace or distance
    ax=None,
    log=False,
    colorbar=True,
    cmap="viridis",
    clip=[0.0, 1.0],
    grid=False,
    grid_color="black",
    grid_linewidth=0.5,
    grid_linestyle=":",
    grid_alpha=1,
    figsize=(10, 6),
    show=True,
    save_path=None,
    dpi=100,
):
    """
    Plot the data in the stream.
    waveform
    wiggles
    """
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

    # init win_axis
    if freq_axis == "x":
        trace_axis = "y"
    elif freq_axis == "y":
        trace_axis = "x"
    else:
        raise ValueError("trace_axis must be 'x' or 'y'")

    # check trace_label
    if trace_label not in ["trace", "interval", "distance"]:
        raise ValueError("trace_label must be 'trace', 'interval' or 'distance'")

    # set times
    starttime_npts = int((starttime - self.stats.starttime) * self.stats.sampling_rate)
    endtime_npts = int((endtime - self.stats.starttime) * self.stats.sampling_rate)
    # npts_times = total_npts_times[starttime_npts:endtime_npts]

    # data
    time_data = self.data[starttrace:endtrace, starttime_npts:endtime_npts].copy()
    data = np.abs(rfft(time_data, axis=1))
    freq = rfftfreq(time_data.shape[1], self.stats.delta)

    # frequency range
    if freqmin is None:
        freqmin = np.min(freq)
    if freqmax is None:
        freqmax = np.max(freq)

    # select data
    freq_mask = (freq >= freqmin) & (freq <= freqmax)
    freq = freq[freq_mask]
    data = data[:, freq_mask]
    if norm_method == "trace":
        # data /= np.max(np.abs(data), axis=1, keepdims=True)
        max_vals = np.max(np.abs(data), axis=1, keepdims=True)
        data = np.where(max_vals != 0, data / max_vals, data)
    elif norm_method == "stream":
        # data /= np.max(np.abs(data))
        max_val = np.max(np.abs(data))
        if max_val != 0:
            data /= max_val
    elif norm_method == "npts":
        # data /= np.max(np.abs(data), axis=0, keepdims=True)
        max_vals = np.max(np.abs(data), axis=0, keepdims=True)
        data = np.where(max_vals != 0, data / max_vals, data)
    else:
        raise ValueError("norm_method must be 'trace' or 'stream'")

    # set ax
    ax = _get_ax(ax, figsize=figsize)

    # plot data
    if freq_axis == "x":
        im = ax.imshow(
            data,
            extent=[freqmin, freqmax, starttrace, endtrace],
            aspect="auto",
            cmap=cmap,
            origin="lower",
        )
    elif freq_axis == "y":
        im = ax.imshow(
            data.T,
            extent=[starttrace, endtrace, freqmin, freqmax],
            aspect="auto",
            cmap=cmap,
            origin="lower",
        )

    else:
        raise ValueError("time_axis must be 'x' or 'y'")

    # clip
    im.set_clim(clip)
    if colorbar:
        plt.colorbar(im, orientation="vertical", ax=ax)

    # grid
    if grid:
        ax.grid(
            color=grid_color,
            linewidth=grid_linewidth,
            linestyle=grid_linestyle,
            alpha=grid_alpha,
        )
    # format axis
    _format_freq_axis(
        ax,
        freqmin,
        freqmax,
        df=freq[1] - freq[0],
        freq_axis=freq_axis,
        freq_ticks=freq_ticks,
        freqtick_rotation=freqtick_rotation,
        freqtick_labelsize=freqtick_labelsize,
    )
    _format_trace_axis(
        ax,
        trace_label,
        self,
        starttrace,
        endtrace,
        trace_ticks,
        trace_axis,
        tracetick_rotation,
        tracetick_labelsize,
    )

    fig = ax.figure
    if freq_axis == "x":
        ax.set_xlim(freqmin, freqmax)
        if log:
            ax.set_xscale("log")
        ax.set_xlabel("Frequency (Hz)")
        if trace_label == "trace":
            ax.set_ylabel("Trace")
        elif trace_label == "distance":
            ax.set_ylabel("Distance (m)")
        elif trace_label == "interval":
            ax.set_ylabel("Interval (m)")
    elif freq_axis == "y":
        if log:
            ax.set_yscale("log")
        ax.set_ylim(freqmin, freqmax)
        ax.set_ylabel("Frequency (Hz)")
        if trace_label == "trace":
            ax.set_xlabel("Trace")
        elif trace_label == "distance":
            ax.set_xlabel("Distance (m)")
        elif trace_label == "interval":
            ax.set_xlabel("Interval (m)")
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
