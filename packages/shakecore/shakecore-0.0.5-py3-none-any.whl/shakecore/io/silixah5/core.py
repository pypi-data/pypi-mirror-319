import re
import h5py
import numpy as np
from obspy import UTCDateTime
from pathlib import Path


def silixah5v1_read(
    pathname_or_url,
    headonly,
    starttrace,
    endtrace,
    steptrace,
    starttime,
    endtime,
):
    pathname_or_url = Path(pathname_or_url)
    match = re.search(r"UTC_(\d{8})_(\d{6}\.\d+)", pathname_or_url.name)
    if match:
        date_part = match.group(1)
        time_part = match.group(2)
        datetime_str = f"{date_part}T{time_part}"
        starttime_raw = UTCDateTime(datetime_str)
    else:
        starttime_raw = UTCDateTime(0)

    with h5py.File(pathname_or_url, "r") as f:
        raw_npts = f["Acoustic"].shape[0]
        trace_num = f["Acoustic"].shape[1]
        sampling_rate = 1000.0
        endtime_raw = UTCDateTime(starttime_raw + raw_npts / sampling_rate)

        if starttrace is None:
            starttrace = 0
        if endtrace is None:
            endtrace = trace_num
        if starttime is None:
            starttime = starttime_raw
        if endtime is None:
            endtime = endtime_raw

        if starttime > endtime_raw or endtime < starttime_raw:
            return None
        else:
            if starttime < starttime_raw:
                starttime = starttime_raw
            if endtime > endtime_raw:
                endtime = endtime_raw
            npts_start = round((starttime - starttime_raw) * sampling_rate)
            npts_end = round((endtime - starttime_raw) * sampling_rate)

        channel = [str(i) for i in np.arange(starttrace, endtrace, steptrace)]

        if headonly:
            data = np.empty((0, 0))
            channel = []
        else:
            data = f["Acoustic"][
                npts_start : npts_end + 1, starttrace:endtrace:steptrace
            ].T

    from shakecore.core.stream import Stream

    header = {
        "starttime": starttime,
        "sampling_rate": sampling_rate,
        "type": "unknown",
        "channel": channel,
    }

    return Stream(data, header)


def silixah5v2_read(
    pathname_or_url,
    headonly,
    starttrace,
    endtrace,
    steptrace,
    starttime,
    endtime,
):
    with h5py.File(pathname_or_url, "r") as f:
        timestamp = np.array(f["Acquisition"]["Raw[0]"]["RawDataTime"]) / 1e6
        raw_npts = len(timestamp)
        sampling_rate = 1 / (timestamp[1] - timestamp[0])
        starttime_raw = UTCDateTime(timestamp[0])
        endtime_raw = UTCDateTime(starttime_raw + raw_npts / sampling_rate)
        trace_num = f["Acquisition"]["Raw[0]"]["RawData"].shape[1]

        if starttrace is None:
            starttrace = 0
        if endtrace is None:
            endtrace = trace_num
        if starttime is None:
            starttime = starttime_raw
        if endtime is None:
            endtime = endtime_raw

        if starttime > endtime_raw or endtime < starttime_raw:
            return None
        else:
            if starttime < starttime_raw:
                starttime = starttime_raw
            if endtime > endtime_raw:
                endtime = endtime_raw
            npts_start = round((starttime - starttime_raw) * sampling_rate)
            npts_end = round((endtime - starttime_raw) * sampling_rate)

        channel = [str(i) for i in np.arange(starttrace, endtrace, steptrace)]

        if headonly:
            data = np.empty((0, 0))
            channel = []
        else:
            data = f["Acquisition"]["Raw[0]"]["RawData"][
                npts_start : npts_end + 1, starttrace:endtrace:steptrace
            ].T

    from shakecore.core.stream import Stream

    header = {
        "starttime": starttime,
        "sampling_rate": sampling_rate,
        "type": "unknown",
        "channel": channel,
    }

    return Stream(data, header)
