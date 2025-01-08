import numpy as np

from shakecore.core.stream import Stream


def rotate(back_azimuth, N=None, E=None, R=None, T=None, method="NE->RT"):
    # check input
    if method == "NE->RT":
        if N is None or E is None:
            raise ValueError("N and E must be given.")

        if N.stats.starttime != E.stats.starttime:
            raise TypeError(
                "Starttime differs: %s vs %s" % (N.stats.starttime, E.stats.starttime)
            )

        if N.stats.endtime != E.stats.endtime:
            raise TypeError(
                "Endtime differs: %s vs %s" % (N.stats.endtime, E.stats.endtime)
            )

        if N.stats.sampling_rate != E.stats.sampling_rate:
            raise TypeError(
                "Sampling rate differs: %s vs %s"
                % (N.stats.sampling_rate, E.stats.sampling_rate)
            )

        if N.stats.trace_num != E.stats.trace_num:
            raise TypeError(
                "Number of traces differs: %s vs %s"
                % (N.stats.trace_num, E.stats.trace_num)
            )

        if N.stats.npts != E.stats.npts:
            raise TypeError(
                "Number of samples differs: %s vs %s" % (N.stats.npts, E.stats.npts)
            )

        if N.stats.type != E.stats.type:
            raise TypeError("Type differs: %s vs %s" % (N.stats.type, E.stats.type))

        if N.data.dtype != E.data.dtype:
            raise TypeError(
                "Data type differs: %s vs %s" % (N.data.dtype, E.data.dtype)
            )

        if N.stats.network != E.stats.network:
            raise TypeError(
                "Network differs: %s vs %s" % (N.stats.network, E.stats.network)
            )

        if N.stats.station != E.stats.station:
            raise TypeError(
                "Station differs: %s vs %s" % (N.stats.station, E.stats.station)
            )
    elif method == "RT->NE":
        if R is None or T is None:
            raise ValueError("R and T must be given.")

        if R.stats.starttime != T.stats.starttime:
            raise TypeError(
                "Starttime differs: %s vs %s" % (R.stats.starttime, T.stats.starttime)
            )

        if R.stats.endtime != T.stats.endtime:
            raise TypeError(
                "Endtime differs: %s vs %s" % (R.stats.endtime, T.stats.endtime)
            )

        if R.stats.sampling_rate != T.stats.sampling_rate:
            raise TypeError(
                "Sampling rate differs: %s vs %s"
                % (R.stats.sampling_rate, T.stats.sampling_rate)
            )

        if R.stats.trace_num != T.stats.trace_num:
            raise TypeError(
                "Number of traces differs: %s vs %s"
                % (R.stats.trace_num, T.stats.trace_num)
            )

        if R.stats.npts != T.stats.npts:
            raise TypeError(
                "Number of samples differs: %s vs %s" % (R.stats.npts, T.stats.npts)
            )

        if R.stats.type != T.stats.type:
            raise TypeError("Type differs: %s vs %s" % (R.stats.type, T.stats.type))

        if R.data.dtype != T.data.dtype:
            raise TypeError(
                "Data type differs: %s vs %s" % (R.data.dtype, T.data.dtype)
            )

        if R.stats.network != T.stats.network:
            raise TypeError(
                "Network differs: %s vs %s" % (R.stats.network, T.stats.network)
            )

        if R.stats.station != T.stats.station:
            raise TypeError(
                "Station differs: %s vs %s" % (R.stats.station, T.stats.station)
            )
    else:
        raise ValueError("method must be 'NE->RT' or 'RT->NE'")

    # task
    BAZ = back_azimuth / 180 * np.pi
    if method == "NE->RT":
        R_data = -np.cos(BAZ) * N.data - np.sin(BAZ) * E.data
        T_data = np.sin(BAZ) * N.data - np.cos(BAZ) * E.data
        R = Stream(data=R_data, header=N.stats)
        T = Stream(data=T_data, header=N.stats)
        R.stats.channel = ["R"] * N.stats.trace_num
        T.stats.channel = ["T"] * N.stats.trace_num
        return R, T
    elif method == "RT->NE":
        N_data = np.sin(BAZ) * T.data - np.cos(BAZ) * R.data
        E_data = -np.cos(BAZ) * T.data - np.sin(BAZ) * R.data
        N = Stream(data=N_data, header=R.stats)
        E = Stream(data=E_data, header=R.stats)
        N.stats.channel = ["N"] * R.stats.trace_num
        E.stats.channel = ["E"] * R.stats.trace_num
        return N, E
