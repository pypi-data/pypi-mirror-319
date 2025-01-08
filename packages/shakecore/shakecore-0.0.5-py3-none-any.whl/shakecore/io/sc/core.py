import json

import h5py
import numpy as np
from obspy import UTCDateTime


def sc_read(
    pathname_or_url,
    headonly,
    starttrace,
    endtrace,
    steptrace,
    starttime,
    endtime,
):
    with h5py.File(pathname_or_url, "r") as f:
        group = f["sc"]
        starttime_raw = UTCDateTime(group.attrs["starttime"])
        endtime_raw = UTCDateTime(group.attrs["endtime"])
        trace_num = group.attrs["trace_num"]
        sampling_rate = group.attrs["sampling_rate"]
        # raw_npts = group.attrs["npts"]

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

        # npts = npts_end - npts_start
        interval = group.attrs["interval"] * steptrace
        type = group.attrs["type"]

        # dynamic parse attributes, [version history reasons]
        network_data = group.attrs["network"]
        if isinstance(network_data, str):  # json format
            network = json.loads(network_data)[starttrace:endtrace:steptrace]
        else:
            network = network_data.tolist()[starttrace:endtrace:steptrace]

        station_data = group.attrs["station"]
        if isinstance(station_data, str):
            station = json.loads(station_data)[starttrace:endtrace:steptrace]
        else:
            station = station_data.tolist()[starttrace:endtrace:steptrace]

        channel_data = group.attrs["channel"]
        if isinstance(channel_data, str):
            channel = json.loads(channel_data)[starttrace:endtrace:steptrace]
        else:
            channel = channel_data.tolist()[starttrace:endtrace:steptrace]

        latitude_data = group.attrs["latitude"]
        if isinstance(latitude_data, str):
            latitude = json.loads(latitude_data)[starttrace:endtrace:steptrace]
        else:
            latitude = latitude_data.tolist()[starttrace:endtrace:steptrace]

        longitude_data = group.attrs["longitude"]
        if isinstance(longitude_data, str):
            longitude = json.loads(longitude_data)[starttrace:endtrace:steptrace]
        else:
            longitude = longitude_data.tolist()[starttrace:endtrace:steptrace]

        elevation_data = group.attrs["elevation"]
        if isinstance(elevation_data, str):
            elevation = json.loads(elevation_data)[starttrace:endtrace:steptrace]
        else:
            elevation = elevation_data.tolist()[starttrace:endtrace:steptrace]

        processing_data = group.attrs["processing"]
        if isinstance(processing_data, str):
            processing = json.loads(processing_data)
        else:
            processing = processing_data.tolist()

        notes = json.loads(group.attrs["notes"])

        # x, y, [version history reasons]
        if "x" in group.attrs:
            x_data = group.attrs["x"]
            if isinstance(x_data, str):
                x = json.loads(x_data)[starttrace:endtrace:steptrace]
            else:
                x = x_data.tolist()[starttrace:endtrace:steptrace]
        else:
            x = [np.nan] * len(network)

        if "y" in group.attrs:
            y_data = group.attrs["y"]
            if isinstance(y_data, str):
                y = json.loads(y_data)[starttrace:endtrace:steptrace]
            else:
                y = y_data.tolist()[starttrace:endtrace:steptrace]
        else:
            y = [np.nan] * len(network)

        # location, [version history reasons]
        if "location" in group.attrs:
            location_data = group.attrs["location"]
            if isinstance(location_data, str):
                location = json.loads(location_data)[starttrace:endtrace:steptrace]
            else:
                location = location_data.tolist()[starttrace:endtrace:steptrace]
        else:
            location = [""] * len(network)

        if headonly:
            data = np.empty((0, 0))
            network = []
            station = []
            location = []
            channel = []
            latitude = []
            longitude = []
            elevation = []
            x = []
            y = []
        else:
            data = group["data"][
                starttrace:endtrace:steptrace, npts_start : npts_end + 1
            ]

    from shakecore.core.stream import Stream

    header = {
        "starttime": starttime,
        "sampling_rate": sampling_rate,
        "interval": float(interval),
        "type": type,
        "network": network,
        "station": station,
        "location": location,
        "channel": channel,
        "latitude": latitude,
        "longitude": longitude,
        "elevation": elevation,
        "x": x,
        "y": y,
        "processing": processing,
        "notes": notes,
    }

    return Stream(data, header)


def sc_write(
    self,
    filename,
):
    with h5py.File(filename, "w") as f:
        group = f.create_group("sc")
        group.attrs["starttime"] = str(self.stats.starttime)
        group.attrs["endtime"] = str(self.stats.endtime)
        group.attrs["sampling_rate"] = self.stats.sampling_rate
        group.attrs["delta"] = self.stats.delta
        group.attrs["interval"] = self.stats.interval
        group.attrs["npts"] = self.stats.npts
        group.attrs["trace_num"] = self.stats.trace_num
        group.attrs["type"] = self.stats.type
        group.attrs["network"] = json.dumps(self.stats.network)
        group.attrs["station"] = json.dumps(self.stats.station)
        group.attrs["location"] = json.dumps(self.stats.location)
        group.attrs["channel"] = json.dumps(self.stats.channel)
        group.attrs["latitude"] = json.dumps(self.stats.latitude)
        group.attrs["longitude"] = json.dumps(self.stats.longitude)
        group.attrs["elevation"] = json.dumps(self.stats.elevation)
        group.attrs["x"] = json.dumps(self.stats.x)
        group.attrs["y"] = json.dumps(self.stats.y)
        group.attrs["processing"] = json.dumps(self.stats.processing)
        group.attrs["notes"] = json.dumps(self.stats.notes)
        group.create_dataset("data", data=self.data)
