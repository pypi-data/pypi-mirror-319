import numpy as np
from geopy.distance import distance

from shakecore.core.utils import _add_processing_info


@_add_processing_info
def mute(self, t1, t2, c1=10000, c2=10000):
    dists_list = []
    trace_num = self.stats.trace_num
    if self.stats.interval is not np.nan:
        for i in range(trace_num):
            dists_list.append(i * self.stats.interval)
    else:
        for i in range(trace_num):
            lat1 = self.stats.latitude[0]
            lon1 = self.stats.longitude[0]
            elev1 = self.stats.elevation[0]
            lat2 = self.stats.latitude[i]
            lon2 = self.stats.longitude[i]
            elev2 = self.stats.elevation[i]
            flat_d = distance((lat1, lon1), (lat2, lon2)).m
            real_d = np.sqrt(flat_d**2 + (elev2 - elev1) ** 2)
            dists_list.append(real_d)

    dists = np.array(dists_list)
    duration = self.stats.npts * self.stats.delta
    dt = self.stats.delta
    for i in range(self.stats.trace_num):
        t_start = t1 + dists[i] / c1
        t_end = t2 + dists[i] / c2
        if t_start < 0:
            t_start = 0
        if t_end > duration:
            t_end = duration

        n_start = int(t_start / dt)
        n_end = int(t_end / dt)

        self.data[i, 0:n_start] = 0
        self.data[i, n_end:] = 0
