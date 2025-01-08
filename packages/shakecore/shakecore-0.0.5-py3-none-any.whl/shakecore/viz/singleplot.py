import matplotlib.pyplot as plt

from .utils.viz_tools import _format_time_axis, _get_ax


def singleplot(
    self,
    starttime=None,
    endtime=None,
    trace=0,
    time_axis="x",
    invert_x=False,
    invert_y=False,
    time_minticks=5,
    time_maxticks=None,
    timetick_rotation=0,
    timetick_labelsize=10,
    ax=None,
    color="black",
    linewidth=1,
    linestyle="-",
    alpha=1,
    fillcolors=(None, None),
    fillalpha=0.5,
    grid=True,
    grid_color="black",
    grid_linewidth=0.5,
    grid_linestyle=":",
    grid_alpha=1,
    figsize=(10, 3),
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

    # check trace
    if trace < 0:
        raise ValueError("trace must be greater than or equal to 0.")
    if trace > self.stats.trace_num:
        raise ValueError("trace must be less than or equal to stream trace_num.")

    # set times
    npts_times = self.times(type="datetime", starttime=starttime, endtime=endtime)
    starttime_npts = int((starttime - self.stats.starttime) * self.stats.sampling_rate)
    endtime_npts = int((endtime - self.stats.starttime) * self.stats.sampling_rate)

    # data
    data = self.data[trace, starttime_npts:endtime_npts].copy()
    network = self.stats.network[trace]
    station = self.stats.station[trace]
    location = self.stats.location[trace]
    channel = self.stats.channel[trace]

    # set ax
    ax = _get_ax(ax, figsize=figsize)
    # plot data
    if time_axis == "x":
        ax.plot(
            npts_times,
            data,
            linewidth=linewidth,
            color=color,
            alpha=alpha,
            linestyle=linestyle,
            label=f"{network}.{station}.{location}.{channel}",
        )
        if fillcolors[0] is not None:
            ax.fill_between(
                npts_times,
                data,
                0,
                where=data > 0,
                facecolor=fillcolors[0],
                alpha=fillalpha,
            )
        if fillcolors[1] is not None:
            ax.fill_between(
                npts_times,
                data,
                0,
                where=data < 0,
                facecolor=fillcolors[1],
                alpha=fillalpha,
            )
    elif time_axis == "y":
        ax.plot(
            data,
            npts_times,
            linewidth=linewidth,
            color=color,
            alpha=alpha,
            linestyle=linestyle,
            label=f"{network}.{station}.{location}.{channel}",
        )
        if fillcolors[0] is not None:
            ax.fill_betweenx(
                npts_times,
                data,
                0,
                where=data > 0,
                facecolor=fillcolors[0],
                alpha=fillalpha,
            )
        if fillcolors[1] is not None:
            ax.fill_betweenx(
                npts_times,
                data,
                0,
                where=data < 0,
                facecolor=fillcolors[1],
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
    props = dict(boxstyle="round", facecolor="w", alpha=0.5)
    ax.text(
        0.03,
        0.96,
        f"{network}.{station}.{location}.{channel}",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=props,
    )

    # format axis
    _format_time_axis(
        ax,
        axis=time_axis,
        tick_rotation=timetick_rotation,
        minticks=time_minticks,
        maxticks=time_maxticks,
        labelsize=timetick_labelsize,
    )

    fig = ax.figure
    if time_axis == "x":
        ax.set_xlim(starttime.datetime, endtime.datetime)
    elif time_axis == "y":
        ax.set_ylim(starttime.datetime, endtime.datetime)
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
