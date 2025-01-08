import copy
import pickle
import warnings

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from obspy import UTCDateTime
from scipy.interpolate import interp1d
from scipy.signal import chirp, correlate, istft, stft
from tqdm import tqdm

from shakecore.viz.utils.viz_tools import _format_time_axis, _get_ax


def read_sov(pilot_file=None, motor_file=None, format="v1"):
    """
    Read SOV file.
    """

    if format == "v1":  # used for "FORGE" project
        sov = SOV()
        if pilot_file is not None:
            pilot_info = np.loadtxt(pilot_file)
            t = pilot_info[:, 0]
            starttime = UTCDateTime(t[0])
            dt = t[1] - t[0]
            h1 = pilot_info[:, 1]
            h2 = pilot_info[:, 2]
            v = pilot_info[:, 3]
            gps_voltage = pilot_info[:, 4]
            sov.add_pilot(starttime, dt, h1, h2, v, gps_voltage, name="pilot_1")

        if motor_file is not None:
            motor_info = np.loadtxt(motor_file, skiprows=2)
            with open(motor_file, "r") as file:
                motor_header = file.readline().strip().split()

            # sov info
            sov_info = motor_header[0].split("_")
            sov_name = sov_info[0].lower()
            sov_series = int(sov_info[1])
            sov_series_number = int(sov_info[2])
            if sov_info[3][0].lower() == "p":
                sov_mode = "production"
            elif sov_info[3][0].lower() == "w":
                sov_mode = "warmup"
            sov.name = sov_name
            sov.mode = sov_mode
            sov.series = sov_series
            sov.series_number = sov_series_number
            sov.direction = motor_header[22].lower()

            # motor info
            start_listen_time = float(motor_header[2])
            end_listen_time = float(motor_header[4])
            large_max_freq = float(motor_header[6])
            large_accelerate_mode = "linear"
            large_accelerate_duration = float(motor_header[8])
            large_hold_mode = "linear"
            large_hold_duration = float(motor_header[10])
            large_decelerate_mode = "linear"
            large_decelerate_duration = float(motor_header[12])
            small_max_freq = float(motor_header[14])
            small_accelerate_mode = "linear"
            small_accelerate_duration = float(motor_header[16])
            samll_hold_mode = "linear"
            small_hold_duration = float(motor_header[18])
            small_decelerate_mode = "linear"
            small_decelerate_duration = float(motor_header[20])
            if motor_info.ndim == 1:
                motor_info = motor_info[np.newaxis, :]
                t = motor_info[:, 0]
                dt = 0.001
            else:
                t = motor_info[:, 0]
                dt = t[1] - t[0]
            starttime = UTCDateTime(t[0])
            large_freq = motor_info[:, 1]
            large_current = motor_info[:, 2]
            large_voltage = motor_info[:, 3]
            small_freq = motor_info[:, 4]
            small_current = motor_info[:, 5]
            small_voltage = motor_info[:, 6]

            sov.add_motor(
                start_listen_time,
                end_listen_time,
                large_max_freq,
                large_accelerate_mode,
                large_accelerate_duration,
                large_hold_mode,
                large_hold_duration,
                large_decelerate_mode,
                large_decelerate_duration,
                starttime,
                dt,
                large_freq,
                large_current,
                large_voltage,
                name="large",
            )
            sov.add_motor(
                start_listen_time,
                end_listen_time,
                small_max_freq,
                small_accelerate_mode,
                small_accelerate_duration,
                samll_hold_mode,
                small_hold_duration,
                small_decelerate_mode,
                small_decelerate_duration,
                starttime,
                dt,
                small_freq,
                small_current,
                small_voltage,
                name="small",
            )

        return sov

    elif format == "v2":
        pass


class Pilot(object):
    def __init__(
        self,
        starttime,
        dt,
        h1=np.array([]),
        h2=np.array([]),
        v=np.array([]),
        gps_voltage=np.array([]),
        name="pilot_1",
    ):
        # h1, perpendicular to the rotary axis of the motor (so horizontal shear is strong)
        # h2, aligned with the rotary axis of the SOV (so should always have the smallest amplitude)
        # v, vertical component
        self.starttime = starttime
        self.dt = dt
        self.npts = max(len(h1), len(h2), len(v))
        self.h1 = h1
        self.h2 = h2
        self.v = v
        self.gps_voltage = gps_voltage
        self.name = name
        self.endtime = starttime + (self.npts - 1) * dt

    def __str__(self):
        pilot = (
            f"* Pilot:\n"
            f"                   name: {self.name}\n"
            f"              starttime: {str(self.starttime)}\n"
            f"                endtime: {str(self.endtime)}\n"
            f"                     dt: {str(self.dt)}\n"
            f"                   npts: {str(self.npts)}\n"
            f"                     h1: {np.array2string(self.h1, threshold=15)}\n"
            f"                     h2: {np.array2string(self.h2, threshold=15)}\n"
            f"                      v: {np.array2string(self.v, threshold=15)}\n"
            f"            gps_voltage: {np.array2string(self.gps_voltage, threshold=15)}\n"
        )
        info = "\n".join([pilot])
        return info

    def __repr__(self):
        return str(self)

    def to_stream(self):

        from shakecore.core.stream import Stream

        data = np.vstack([self.h1, self.h2, self.v])
        header = {
            "starttime": self.starttime,
            "delta": self.dt,
            "station": [self.name, self.name, self.name],
            "channel": ["H1", "H2", "V"],
        }
        stream = Stream(data=data, header=header)
        return stream

    def plot(
        self,
        starttime=None,
        endtime=None,
        time_minticks=5,
        time_maxticks=None,
        timetick_rotation=0,
        timetick_labelsize=10,
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
        figsize=(10, 5),
        show=True,
        save_path=None,
        dpi=100,
    ):
        # check starttime and endtime
        if starttime is None:
            starttime = self.starttime
        if starttime < self.starttime:
            raise ValueError(
                "starttime must be greater than or equal to stream starttime."
            )
        if endtime is None:
            endtime = self.endtime
        if endtime > self.endtime:
            raise ValueError("endtime must be less than or equal to stream endtime.")

        # set times
        npts = round((endtime - starttime) / self.dt)
        time_array = np.arange(npts)
        time_array = time_array * self.dt
        time_deltas_ns = (time_array * 1e9).astype(np.int64)
        time_deltas_timedelta64 = time_deltas_ns * np.timedelta64(1, "ns")
        datetime_array = np.datetime64(starttime.datetime) + time_deltas_timedelta64
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            npts_times = pd.Series(datetime_array).dt.to_pydatetime()
            npts_times = np.array(npts_times)
        starttime_npts = round((starttime - self.starttime) / self.dt)
        endtime_npts = round((endtime - self.starttime) / self.dt)

        # data
        h1 = self.h1[starttime_npts:endtime_npts].copy()
        h2 = self.h2[starttime_npts:endtime_npts].copy()
        v = self.v[starttime_npts:endtime_npts].copy()

        # set ax
        fig, axs = plt.subplots(
            3,
            1,
            figsize=figsize,
            sharex="col",
            gridspec_kw=dict(height_ratios=[1, 1, 1]),
        )
        fig.subplots_adjust(hspace=0)

        # plot data
        data = [h1, h2, v]
        for i in range(3):
            axs[i].plot(
                npts_times,
                data[i],
                linewidth=linewidth,
                color=color,
                alpha=alpha,
                linestyle=linestyle,
            )
            if fillcolors[0] is not None:
                axs[i].fill_between(
                    npts_times,
                    data[i],
                    0,
                    where=data[i] > 0,
                    facecolor=fillcolors[0],
                    alpha=fillalpha,
                )
            if fillcolors[1] is not None:
                axs[i].fill_between(
                    npts_times,
                    data[i],
                    0,
                    where=data[i] < 0,
                    facecolor=fillcolors[1],
                    alpha=fillalpha,
                )

            # grid
            if grid:
                axs[i].grid(
                    color=grid_color,
                    linewidth=grid_linewidth,
                    linestyle=grid_linestyle,
                    alpha=grid_alpha,
                )

        # format axis
        _format_time_axis(
            axs[2],
            axis="x",
            tick_rotation=timetick_rotation,
            minticks=time_minticks,
            maxticks=time_maxticks,
            labelsize=timetick_labelsize,
        )

        axs[0].set_ylabel("H1")
        axs[1].set_ylabel("H2")
        axs[2].set_ylabel("V")

        # set axis limits
        scale = 1.4
        y_abs_max = max([np.max(np.abs(h1)), np.max(np.abs(h2)), np.max(np.abs(v))])
        axs[0].set_ylim(-y_abs_max * scale, y_abs_max * scale)
        axs[1].set_ylim(-y_abs_max * scale, y_abs_max * scale)
        axs[2].set_ylim(-y_abs_max * scale, y_abs_max * scale)
        axs[2].set_xlim(starttime.datetime, endtime.datetime)

        if not show:
            plt.close(fig)
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return axs

    def spectrogram(
        self,
        component="v",
        dense_N=1,
        freqmin=None,
        freqmax=None,
        method="stft",  # 'stft', 'wavelet', and 'stockwell'
        starttime=None,
        endtime=None,
        color="black",
        linewidth=1,
        linestyle="-",
        alpha=1,
        fillcolors=(None, None),
        fillalpha=0.5,
        colorbar=True,
        cmap="viridis",  # "jet", "bwr", "seismic", "viridis"
        clip=[0.0, 1.0],
        time_minticks=5,
        time_maxticks=None,
        timetick_rotation=0,
        timetick_labelsize=10,
        log=False,
        grid=False,
        grid_color="black",
        grid_linewidth=0.5,
        grid_linestyle=":",
        grid_alpha=1,
        figsize=(10, 5),
        show=True,
        save_path=None,
        dpi=100,
    ):

        # check data
        if component == "h1":
            data = self.h1.copy()
        elif component == "h2":
            data = self.h2.copy()
        elif component == "v":
            data = self.v.copy()
        data = data[np.newaxis, :]

        # stream
        from shakecore.core.stream import Stream

        stream = Stream(
            data=data, header={"starttime": self.starttime, "delta": self.dt}
        )
        axs = stream.viz.spectrogram(
            trace=0,
            freqmin=freqmin,
            freqmax=freqmax,
            method=method,
            dense_N=dense_N,
            starttime=starttime,
            endtime=endtime,
            color=color,
            linewidth=linewidth,
            linestyle=linestyle,
            alpha=alpha,
            fillcolors=fillcolors,
            fillalpha=fillalpha,
            colorbar=colorbar,
            cmap=cmap,
            clip=clip,
            time_minticks=time_minticks,
            time_maxticks=time_maxticks,
            timetick_rotation=timetick_rotation,
            timetick_labelsize=timetick_labelsize,
            log=log,
            grid=grid,
            grid_color=grid_color,
            grid_linewidth=grid_linewidth,
            grid_linestyle=grid_linestyle,
            grid_alpha=grid_alpha,
            figsize=figsize,
            show=show,
            save_path=None,
            dpi=dpi,
        )

        axs[0].set_title(f"{component.upper()} component")

        if save_path is not None:
            fig = axs[0].figure
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return axs[0], axs[1]


class Motor(object):
    def __init__(
        self,
        start_listen_time,
        end_listen_time,
        max_freq,
        accelerate_mode,
        accelerate_duration,
        hold_mode,
        hold_duration,
        decelerate_mode,
        decelerate_duration,
        starttime,
        dt,
        freq=np.array([]),
        current=np.array([]),
        voltage=np.array([]),
        name="Large",
    ):
        self.npts = len(freq)
        self.endtime = starttime + (self.npts - 1) * dt
        self.start_listen_time = start_listen_time
        self.end_listen_time = end_listen_time
        self.max_freq = max_freq
        self.accelerate_mode = accelerate_mode
        self.accelerate_duration = accelerate_duration
        self.hold_mode = hold_mode
        self.hold_duration = hold_duration
        self.decelerate_mode = decelerate_mode
        self.decelerate_duration = decelerate_duration
        self.starttime = starttime
        self.dt = dt
        self.freq = freq
        self.current = current
        self.voltage = voltage
        self.name = name

    def __str__(self):
        motor = (
            f"* Motor:\n"
            f"                   name: {self.name}\n"
            f"              starttime: {str(self.starttime)}\n"
            f"                endtime: {str(self.endtime)}\n"
            f"                     dt: {str(self.dt)}\n"
            f"                   npts: {str(self.npts)}\n"
            f"      start_listen_time: {str(self.start_listen_time)}\n"
            f"        end_listen_time: {str(self.end_listen_time)}\n"
            f"               max_freq: {str(self.max_freq)}\n"
            f"        accelerate_mode: {str(self.accelerate_mode)}\n"
            f"    accelerate_duration: {str(self.accelerate_duration)}\n"
            f"              hold_mode: {str(self.hold_mode)}\n"
            f"          hold_duration: {str(self.hold_duration)}\n"
            f"        decelerate_mode: {str(self.decelerate_mode)}\n"
            f"    decelerate_duration: {str(self.decelerate_duration)}\n"
            f"                   freq: {np.array2string(self.freq, threshold=15)}\n"
            f"                current: {np.array2string(self.current, threshold=15)}\n"
            f"                voltage: {np.array2string(self.voltage, threshold=15)}\n"
        )
        info = "\n".join([motor])
        return info

    def __repr__(self):
        return str(self)

    def forward(self, sampling_rate=None, direction="forward"):
        if sampling_rate is None:
            sampling_rate = 4 * self.max_freq

        dt = 1 / sampling_rate
        t_accelerate = np.arange(0, self.accelerate_duration, dt)
        t_hold = np.arange(0, self.hold_duration, dt)
        t_decelerate = np.arange(0, self.decelerate_duration + dt, dt)

        sweep_signal_startlisten = np.zeros(int(self.start_listen_time / dt))
        sweep_signal_endlisten = np.zeros(int(self.end_listen_time / dt))
        if self.accelerate_duration != 0:
            amp = np.linspace(0, self.max_freq, len(t_accelerate))
            sweep_signal_accelerate = amp**2 * chirp(
                t_accelerate,
                f0=0,
                f1=self.max_freq,
                t1=self.accelerate_duration,
                method=self.accelerate_mode,
            )
        else:
            sweep_signal_accelerate = np.array([])

        if self.hold_duration != 0:
            amp = np.linspace(self.max_freq, self.max_freq, len(t_hold))
            sweep_signal_hold = amp**2 * chirp(
                t_hold,
                f0=self.max_freq,
                f1=self.max_freq,
                t1=self.hold_duration,
                method=self.hold_mode,
            )
        else:
            sweep_signal_hold = np.array([])

        if self.decelerate_duration != 0:
            amp = np.linspace(self.max_freq, 0, len(t_decelerate))
            sweep_signal_decelerate = amp**2 * chirp(
                t_decelerate,
                f0=self.max_freq,
                f1=0,
                t1=self.decelerate_duration,
                method=self.decelerate_mode,
            )

        else:
            sweep_signal_decelerate = np.array([])

        sweep_signal = np.concatenate(
            [
                sweep_signal_startlisten,
                sweep_signal_accelerate,
                sweep_signal_hold,
                sweep_signal_decelerate,
                sweep_signal_endlisten,
            ]
        )

        from shakecore.core.stream import Stream

        header = {
            "starttime": self.starttime,
            "sampling_rate": sampling_rate,
            "station": ["pilot_virtual"],
            "channel": ["motor_" + self.name],
        }
        stream = Stream(data=sweep_signal[np.newaxis, :], header=header)

        if direction == "reverse":
            stream.data *= -1

        return stream

    def plot(
        self,
        component="freq",
        starttime=None,
        endtime=None,
        time_minticks=5,
        time_maxticks=None,
        timetick_rotation=0,
        timetick_labelsize=10,
        ax=None,
        color="black",
        linewidth=1,
        linestyle="-",
        alpha=1,
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
        if component == "freq":
            data = self.freq
        elif component == "current":
            data = self.current
        elif component == "voltage":
            data = self.voltage

        # check starttime and endtime
        if starttime is None:
            starttime = self.starttime
        if starttime < self.starttime:
            raise ValueError(
                "starttime must be greater than or equal to stream starttime."
            )
        if endtime is None:
            endtime = self.endtime
        if endtime > self.endtime:
            raise ValueError("endtime must be less than or equal to stream endtime.")

        # set times
        npts = round((endtime - starttime) / self.dt)
        time_array = np.arange(npts)
        time_array = time_array * self.dt
        time_deltas_ns = (time_array * 1e9).astype(np.int64)
        time_deltas_timedelta64 = time_deltas_ns * np.timedelta64(1, "ns")
        datetime_array = np.datetime64(starttime.datetime) + time_deltas_timedelta64
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            npts_times = pd.Series(datetime_array).dt.to_pydatetime()
            npts_times = np.array(npts_times)
        starttime_npts = round((starttime - self.starttime) / self.dt)
        endtime_npts = round((endtime - self.starttime) / self.dt)

        # data
        data = data[starttime_npts:endtime_npts].copy()

        # set ax
        ax = _get_ax(ax, figsize=figsize)

        # plot data
        ax.plot(
            npts_times,
            data,
            linewidth=linewidth,
            color=color,
            alpha=alpha,
            linestyle=linestyle,
            label=self.name,
        )

        # grid
        if grid:
            ax.grid(
                color=grid_color,
                linewidth=grid_linewidth,
                linestyle=grid_linestyle,
                alpha=grid_alpha,
            )

        # format axis
        _format_time_axis(
            ax,
            axis="x",
            tick_rotation=timetick_rotation,
            minticks=time_minticks,
            maxticks=time_maxticks,
            labelsize=timetick_labelsize,
        )

        if component == "freq":
            ax.set_ylabel("Frequency (Hz)")
        elif component == "current":
            ax.set_ylabel("Current (A)")
        elif component == "voltage":
            ax.set_ylabel("Voltage (V)")

        # set axis limits
        ax.set_xlim(starttime.datetime, endtime.datetime)
        ax.legend(loc="upper right", fontsize=8, shadow=False)

        fig = ax.figure
        if not show:
            plt.close(fig)
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return ax


class SOV(object):
    def __init__(
        self,
        name="sov",
        mode="production",
        series=1,
        series_number=1,
        direction="forward",
    ):
        self.name = name
        self.mode = mode
        self.series = series
        self.series_number = series_number
        self.direction = direction
        self.motor = []
        self.pilot = []
        self.motor_num = len(self.motor)
        self.pilot_num = len(self.pilot)

    def __str__(self):
        sov = (
            f"* SOV:\n"
            f"                   name: {self.name}\n"
            f"                   mode: {self.mode}\n"
            f"                 series: {self.series}\n"
            f"          series_number: {self.series_number}\n"
            f"              direction: {self.direction}\n"
        )

        if self.motor_num == 0:
            motor = "No motor info.\n"
        else:
            motor = ""
            for i in range(self.motor_num):
                motor += str(self.motor[i]) + "\n"

        if self.pilot_num == 0:
            pilot = "No pilot info.\n"
        else:
            pilot = ""
            for i in range(self.pilot_num):
                pilot += str(self.pilot[i]) + "\n"

        info = "\n".join([sov, motor, pilot])
        return info

    def __repr__(self):
        return str(self)

    def copy(self):
        return copy.deepcopy(self)

    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    def add_motor(
        self,
        start_listen_time,
        end_listen_time,
        max_freq,
        accelerate_mode,
        accelerate_duration,
        hold_mode,
        hold_duration,
        decelerate_mode,
        decelerate_duration,
        starttime,
        dt,
        freq=np.array([]),
        current=np.array([]),
        voltage=np.array([]),
        name="large",
    ):
        motor = Motor(
            start_listen_time,
            end_listen_time,
            max_freq,
            accelerate_mode,
            accelerate_duration,
            hold_mode,
            hold_duration,
            decelerate_mode,
            decelerate_duration,
            starttime,
            dt,
            freq,
            current,
            voltage,
            name,
        )
        self.motor.append(motor)
        self.motor_num += 1

    def add_pilot(
        self,
        starttime,
        dt,
        h1=np.array([]),
        h2=np.array([]),
        v=np.array([]),
        gps_voltage=np.array([]),
        name="pilot_1",
    ):
        pilot = Pilot(starttime, dt, h1, h2, v, gps_voltage, name)
        self.pilot.append(pilot)
        self.pilot_num += 1

    def plot_motor(
        self,
        component="freq",
        starttime=None,
        endtime=None,
        time_minticks=5,
        time_maxticks=None,
        timetick_rotation=0,
        timetick_labelsize=10,
        ax=None,
        linewidth=1,
        linestyle="-",
        alpha=1,
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
        ax = _get_ax(ax=ax, figsize=figsize)
        color = list(mcolors.TABLEAU_COLORS.keys())
        color_num = len(color)
        for i in range(self.motor_num):
            ax = self.motor[i].plot(
                component=component,
                starttime=starttime,
                endtime=endtime,
                time_minticks=time_minticks,
                time_maxticks=time_maxticks,
                timetick_rotation=timetick_rotation,
                timetick_labelsize=timetick_labelsize,
                ax=ax,
                color=color[i % color_num],
                linewidth=linewidth,
                linestyle=linestyle,
                alpha=alpha,
                grid=grid,
                grid_color=grid_color,
                grid_linewidth=grid_linewidth,
                grid_linestyle=grid_linestyle,
                grid_alpha=grid_alpha,
                show=show,
                save_path=None,
            )

        if save_path is not None:
            fig = ax.figure
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return ax

    def pilot_forward(self, sampling_rate=None, stack=True, direction="forward"):
        if self.motor_num == 0:
            raise ValueError("No motor info.")

        if stack:
            motor = self.motor[0]
            stream = motor.forward(sampling_rate)
            stream.stats.station = ["pilot_virtual"]
            stream.stats.channel = ["motor_stack"]
            if self.motor_num > 1:
                for i in range(1, self.motor_num):
                    new_stream = self.motor[i].forward(sampling_rate, direction)
                    stream.data += new_stream.data
        else:
            motor = self.motor[0]
            stream = motor.forward(sampling_rate)
            for i in range(1, self.motor_num):
                stream.extend(self.motor[i].forward(sampling_rate, direction))

        return stream

    def pilot_to_pool(self):
        from shakecore.core.pool import Pool

        pool = Pool()
        for i in range(self.pilot_num):
            stream = self.pilot[i].to_stream()
            pool.append(stream)
        return pool

    def tv_filter_pilot(
        self,
        pilot_index=0,
        component="v",
        f_collar=5,
        f_slope=1,
        stft_twin=2,
        tshift=0,
        dev_t_max=5,  # seconds
    ):
        # check motor VFD data
        for i in range(0, self.motor_num):
            dev_t1 = abs(self.pilot[pilot_index].starttime - self.motor[i].starttime)
            dev_t2 = abs(self.pilot[pilot_index].endtime - self.motor[i].endtime)
            if len(self.motor[i].freq) == 0:
                raise ValueError("Motor VFD freq data is empty.")
            if dev_t1 > dev_t_max or dev_t2 > dev_t_max:
                raise ValueError("Motor VFD data is not in the time range of pilot.")

        # generate filter
        fs = 1 / self.pilot[pilot_index].dt
        nperseg = int(stft_twin * fs)
        if component == "h1":
            data = self.pilot[pilot_index].h1
        elif component == "h2":
            data = self.pilot[pilot_index].h2
        elif component == "v":
            data = self.pilot[pilot_index].v
        f, t, Zxx = stft(data, fs=fs, nperseg=nperseg)
        stft_dt = t[1] - t[0]
        tf_filter = np.zeros((len(f), len(t)))
        for i in range(0, self.motor_num):
            vfd_freq = self.motor[i].freq
            vfd_dt = self.motor[i].dt
            dev_t = self.motor[i].starttime - self.pilot[pilot_index].starttime
            interp = interp1d(
                dev_t + np.arange(0, len(vfd_freq)) * vfd_dt,
                vfd_freq,
                kind="linear",
                bounds_error=False,
                fill_value="extrapolate",
            )
            freq = interp(t)
            for j in range(0, len(t)):
                f2 = freq[j] - f_collar / 2
                f3 = freq[j] + f_collar / 2
                f1 = f2 - f_slope
                f4 = f3 + f_slope
                f_interp = interp1d(
                    [f1, f2, f3, f4],
                    [0, 1, 1, 0],
                    kind="linear",
                    bounds_error=False,
                    fill_value=0,
                )
                tf_filter[(f >= f1) & (f <= f4), j] = f_interp(f[(f >= f1) & (f <= f4)])

        tf_filter[tf_filter > 1] = 1

        # shift tf_filter
        tshift_npts = int(tshift / stft_dt)
        if tshift_npts > 0:
            tf_filter_shift = np.zeros_like(tf_filter)
            tf_filter_shift[:, :tshift_npts] = np.finfo(float).eps
            tf_filter_shift[:, tshift_npts:] = tf_filter[:, :-tshift_npts]
        else:
            tf_filter_shift = tf_filter

        # apply filter
        Zxx = Zxx * tf_filter_shift

        # inverse stft
        _, data_new = istft(Zxx, fs=fs)

        if component == "h1":
            self.pilot[pilot_index].h1 = data_new
        elif component == "h2":
            self.pilot[pilot_index].h2 = data_new
        elif component == "v":
            self.pilot[pilot_index].v = data_new

    def tv_filter(
        self,
        stream,
        f_collar=5,
        f_slope=1,
        stft_twin=2,
        calibrate_tshift=False,
        dev_t_max=5,  # seconds
        jobs=1,
        flag=True,
    ):
        # check motor VFD data
        for i in range(0, self.motor_num):
            dev_t1 = abs(stream.stats.starttime - self.motor[i].starttime)
            dev_t2 = abs(stream.stats.endtime - self.motor[i].endtime)
            if len(self.motor[i].freq) == 0:
                raise ValueError("Motor VFD freq data is empty.")
            if dev_t1 > dev_t_max or dev_t2 > dev_t_max:
                raise ValueError("Motor VFD data is not in the time range of stream.")

        # initialize output_data
        stream_new = stream.copy()

        # generate filter
        fs = 1 / stream.stats.delta
        nperseg = int(stft_twin * fs)
        f, t, _ = stft(stream_new.data[0], fs=fs, nperseg=nperseg)
        stft_dt = t[1] - t[0]
        tf_filter = np.zeros((len(f), len(t)))
        for i in range(0, self.motor_num):
            vfd_freq = self.motor[i].freq
            vfd_dt = self.motor[i].dt
            dev_t = self.motor[i].starttime - stream.stats.starttime
            interp = interp1d(
                dev_t + np.arange(0, len(vfd_freq)) * vfd_dt,
                vfd_freq,
                kind="linear",
                bounds_error=False,
                fill_value="extrapolate",
            )
            freq = interp(t)
            for j in range(0, len(t)):
                f2 = freq[j] - f_collar / 2
                f3 = freq[j] + f_collar / 2
                f1 = f2 - f_slope
                f4 = f3 + f_slope
                f_interp = interp1d(
                    [f1, f2, f3, f4],
                    [0, 1, 1, 0],
                    kind="linear",
                    bounds_error=False,
                    fill_value=0,
                )
                tf_filter[(f >= f1) & (f <= f4), j] = f_interp(f[(f >= f1) & (f <= f4)])

        tf_filter[tf_filter > 1] = 1

        # initialize pbar
        trace_num = stream.stats.trace_num
        if flag:
            pbar = tqdm(range(0, trace_num), desc=f"Run via {jobs} jobs in CPU")
        else:
            pbar = range(0, trace_num)

        if calibrate_tshift:
            tshifts = stream.stats.notes["calibrate_tshift"]
        else:
            tshifts = np.zeros(trace_num)

        results = []
        if jobs == 1:
            for i in pbar:
                result = self.tv_filter_job(
                    stream_new.data[i],
                    fs,
                    tf_filter,
                    nperseg,
                    int(tshifts[i] / stft_dt),
                )
                results.append(result)
        elif jobs > 1:
            results = Parallel(n_jobs=jobs, backend="loky")(
                delayed(self.tv_filter_job)(
                    stream_new.data[i],
                    fs,
                    tf_filter,
                    nperseg,
                    int(tshifts[i] / stft_dt),
                )
                for i in pbar
            )
        else:
            raise ValueError("'jobs' must be larger than 0.")

        stream_new.data = np.array(results)

        # close pbar
        if flag:
            pbar.close()

        return stream_new

    def tv_filter_job(self, data, fs, tf_filter, nperseg, tshift_npts):
        _, _, Zxx = stft(data, fs=fs, nperseg=nperseg)

        # shift tf_filter
        if tshift_npts > 0:
            tf_filter_shift = np.zeros_like(tf_filter)
            tf_filter_shift[:, :tshift_npts] = np.finfo(float).eps
            tf_filter_shift[:, tshift_npts:] = tf_filter[:, :-tshift_npts]
        else:
            tf_filter_shift = tf_filter

        # apply filter
        Zxx = Zxx * tf_filter_shift

        # inverse stft
        _, data_new = istft(Zxx, fs=fs)

        return data_new

    def rm_response(
        self,
        stream,
        pilot_num=0,
        component="v",
        method="deconv",  # 'deconv', 'coherency', 'xcorr', or 'xcorr_my'
        water_level=0.01,
        pre_normalize=False,
        jobs=1,
        flag=True,
    ):
        # check
        if stream.stats.delta != self.pilot[pilot_num].dt:
            raise ValueError("sampling rate of stream and pilot must be the same.")

        if stream.stats.starttime != self.pilot[pilot_num].starttime:
            raise ValueError("starttime of stream and pilot must be the same.")

        if stream.stats.endtime != self.pilot[pilot_num].endtime:
            warnings.warn(
                "the duration of stream and pilot are different, and we recommend to use the same duration, otherwise the result may be incorrect when stream duration is very short."
            )

        # initialize output_data
        stream_new = stream.copy()

        # initialize pbar
        trace_num = stream.stats.trace_num
        if flag:
            pbar = tqdm(range(0, trace_num), desc=f"Run via {jobs} jobs in CPU")
        else:
            pbar = range(0, trace_num)

        results = []
        if jobs == 1:
            for i in pbar:
                result = self.rm_response_job(
                    stream_new.data[i],
                    pilot_num,
                    component,
                    method,
                    water_level,
                    pre_normalize,
                )
                results.append(result)
        elif jobs > 1:
            results = Parallel(n_jobs=jobs, backend="loky")(
                delayed(self.rm_response_job)(
                    stream_new.data[i],
                    pilot_num,
                    component,
                    method,
                    water_level,
                    pre_normalize,
                )
                for i in pbar
            )
        else:
            raise ValueError("'jobs' must be larger than 0.")

        stream_new.data = np.array(results)

        # close pbar
        if flag:
            pbar.close()

        return stream_new

    def rm_response_job(
        self, data, pilot_num, component, method, water_level, pre_normalize
    ):
        # check sweep_signal
        if component == "h1":
            sweep_signal = self.pilot[pilot_num].h1
        elif component == "h2":
            sweep_signal = self.pilot[pilot_num].h2
        elif component == "v":
            sweep_signal = self.pilot[pilot_num].v

        if pre_normalize:
            data = data / np.max(np.abs(data))
            sweep_signal = sweep_signal / np.max(np.abs(sweep_signal))

        # remove source signature
        if method == "deconv":
            length = np.max([len(sweep_signal), len(data)])
            S = np.fft.rfft(sweep_signal, n=length)
            R = np.fft.rfft(data, n=length)
            S2 = S * np.conj(S)
            rfft_deconv = R * np.conj(S) / (S2 + water_level * np.mean(S2))
            gf = np.fft.irfft(rfft_deconv).real

        elif method == "coherency":
            length = np.max([len(sweep_signal), len(data)])
            S = np.fft.rfft(sweep_signal, n=length)
            R = np.fft.rfft(data, n=length)
            SR = np.abs(S) * np.abs(R)
            rfft_coherency = R * np.conj(S) / (SR + water_level * np.mean(SR))
            gf = np.fft.irfft(rfft_coherency).real

        elif method == "xcorr":
            gf = correlate(data, sweep_signal, mode="full")
            gf = gf[len(sweep_signal) :]

        elif method == "xcorr_my":
            if len(data) < len(sweep_signal):
                data_new = np.pad(data, (0, len(sweep_signal) - len(data)))
                sweep_signal_new = sweep_signal
            elif len(data) > len(sweep_signal):
                data_new = data
                sweep_signal_new = np.pad(
                    sweep_signal, (0, len(data) - len(sweep_signal))
                )
            else:
                data_new = data
                sweep_signal_new = sweep_signal

            R = np.fft.rfft(data_new)
            S = np.fft.rfft(sweep_signal_new)
            rfft_corr = R * np.conj(S)
            gf = np.fft.irfft(rfft_corr).real

        else:
            raise ValueError(
                "method must be 'xcorr', 'deconv', 'coherency', or 'xcorr_my'."
            )

        return gf
