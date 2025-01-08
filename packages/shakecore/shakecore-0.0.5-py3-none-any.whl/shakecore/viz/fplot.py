import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import rfft, rfftfreq

from .utils.viz_tools import _format_freq_axis, _format_trace_axis, _get_ax


def fplot(
    self,
    freqmin=None,
    freqmax=None,
    starttime=None,
    endtime=None,
    starttrace=None,
    endtrace=None,
    norm_method="stream",  # trace or stream
    amp_scale=1,
    freq_axis="x",
    invert_x=False,
    invert_y=False,
    freq_ticks=5,
    freqtick_rotation=0,
    freqtick_labelsize=10,
    trace_ticks=5,
    tracetick_rotation=0,
    tracetick_labelsize=10,
    trace_label="trace",  # 'trace'  "interval", or 'distance'
    ax=None,
    log=False,
    color="black",
    linewidth=1,
    linestyle="-",
    alpha=1,
    fillcolor=None,
    fillalpha=0.5,
    grid=True,
    grid_color="black",
    grid_linewidth=0.5,
    grid_linestyle=":",
    grid_alpha=1,
    figsize=(10, 5),
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
        data = data / (np.max(np.abs(data), axis=1, keepdims=True) * 2)
    elif norm_method == "stream":
        data = data / (np.max(np.abs(data)) * 2)
    else:
        raise ValueError("norm_method must be 'trace' or 'stream'")

    # set ax
    ax = _get_ax(ax, figsize=figsize)
    # plot data
    for i in range(0, endtrace - starttrace):
        shift = i + starttrace
        if freq_axis == "x":
            ax.plot(
                freq,
                data[i, :] * amp_scale + shift,
                linewidth=linewidth,
                color=color,
                alpha=alpha,
                linestyle=linestyle,
            )
            if fillcolor is not None:
                ax.fill_between(
                    freq,
                    data[i, :] * amp_scale + shift,
                    shift,
                    where=data[i, :] * amp_scale + shift > shift,
                    facecolor=fillcolor,
                    alpha=fillalpha,
                )

        elif freq_axis == "y":
            ax.plot(
                data[i, :] * amp_scale + shift,
                freq,
                linewidth=linewidth,
                color=color,
                alpha=alpha,
                linestyle=linestyle,
            )
            if fillcolor is not None:
                ax.fill_betweenx(
                    freq,
                    data[i, :] * amp_scale + shift,
                    shift,
                    where=data[i, :] * amp_scale + shift > shift,
                    facecolor=fillcolor,
                    alpha=fillalpha,
                )

        else:
            raise ValueError("time_axis must be 'x' or 'y'")
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
        ax.set_ylim(freqmin, freqmax)
        if log:
            ax.set_yscale("log")
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
