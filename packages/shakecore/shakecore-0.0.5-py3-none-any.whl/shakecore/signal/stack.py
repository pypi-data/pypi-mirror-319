import numpy as np
from joblib import Parallel, delayed
from obspy import UTCDateTime
from scipy.fftpack import next_fast_len
from scipy.signal import hilbert
from tqdm import tqdm


def pws_cpu(data, p=2):
    """
    Performs phase-weighted stack on array of time series. Modified on the noise function by Tim Climents.
    Follows methods of Schimmel and Paulssen, 1997.
    If s(t) is time series data (seismogram, or cross-correlation),
    S(t) = s(t) + i*H(s(t)), where H(s(t)) is Hilbert transform of s(t)
    S(t) = s(t) + i*H(s(t)) = A(t)*exp(i*phi(t)), where
    A(t) is envelope of s(t) and phi(t) is phase of s(t)
    Phase-weighted stack, g(t), is then:
    g(t) = 1/N sum j = 1:N s_j(t) * | 1/N sum k = 1:N exp[i * phi_k(t)]|^v
    where N is number of traces used, v is sharpness of phase-weighted stack

    PARAMETERS:
    ---------------------
    data: N length array of time series data (numpy.ndarray)
    p: exponent for phase stack (int). default is 2

    RETURNS:
    ---------------------
    outdata: Phase weighted stack of time series data (numpy.ndarray)
    """

    if data.ndim == 1:
        print("2D matrix is needed")
        return data
    N, M = data.shape
    if N >= 2:
        analytic = hilbert(data, axis=1, N=next_fast_len(M))[:, :M]
        phase = np.angle(analytic)
        phase_stack = np.mean(np.exp(1j * phase), axis=0)
        phase_stack = np.abs(phase_stack) ** (p)

        weighted = np.multiply(data, phase_stack)

        outdata = np.mean(weighted, axis=0)
    else:
        outdata = data[0].copy()
    return outdata


def pws_cuda(data, p=2):
    pass


def slice_window(npts, segment_points, step_points):
    if segment_points < npts:
        slide_points = segment_points - step_points
        win_num = 0
        for i in range(0, int(npts / slide_points)):
            if (i * slide_points + segment_points) <= npts:
                win_num += 1
            else:
                break
        win_info = np.empty((win_num, 2), dtype=int)
        for i in range(win_num):
            win_info[i, 0] = i * slide_points
            win_info[i, 1] = i * slide_points + segment_points
    elif segment_points == npts:
        win_num = 1
        win_info = np.array([[0, npts]], dtype=int)
    else:
        raise ValueError(
            "error: segment-points length is larger than npts when slicing windows!"
        )

    return win_info


def process_cpu(data, method, config, win_info):
    if method == "linear":
        npts = data.shape[1]
        stack_win_num = win_info.shape[0]
        result = np.empty((stack_win_num, npts), dtype=float)
        for i in range(0, stack_win_num):
            result[i] = np.mean(data[win_info[i, 0] : win_info[i, 1], :], axis=0)
    elif method == "pws":
        p = config["p"]
        npts = data.shape[1]
        stack_win_num = win_info.shape[0]
        result = np.empty((stack_win_num, npts), dtype=float)
        for i in range(0, stack_win_num):
            result[i] = pws_cpu(data[win_info[i, 0] : win_info[i, 1], :], p)

    return result


def process_cuda(data, method, config, win_info):
    pass


def stack(
    self,
    method="linear",  # 'linear' or 'pws'
    config={"p": 2},
    mode="all",  # 'all', 'num', or 'time'
    time_len=60 * 60,  # in seconds
    time_step=30 * 60,
    num_len=10,  # in number of traces
    num_step=5,
    device="cpu",
    jobs=1,  # for number of traces
    flag=True,
):
    stream_num = len(self)
    trace_num = self[0].stats.trace_num
    npts = self[0].stats.npts
    if device == "cpu":
        if mode == "all":
            win_info = np.array([[0, stream_num]])
        elif mode == "num":
            win_info = slice_window(stream_num, num_len, num_step)
        elif mode == "time":
            duration = self[-1].stats.starttime - self[0].stats.starttime
            win_info_time = slice_window(duration, time_len, time_step)
            win_num = win_info_time.shape[0]
            win_info = np.empty((win_num, 2), dtype=int)
            for i in range(0, win_num):
                for j in range(0, stream_num):
                    if (
                        self[j].stats.starttime
                        >= self[0].stats.starttime + win_info_time[i, 0]
                    ):
                        win_info[i, 0] = j
                        break
                for j in range(0, stream_num):
                    if (
                        self[j].stats.starttime
                        >= self[0].stats.starttime + win_info_time[i, 1]
                    ):
                        win_info[i, 1] = j
                        break

            win_info = np.unique(win_info, axis=0)

        # init data
        new_stream_num = win_info.shape[0]
        data = np.empty((trace_num, stream_num, npts), dtype=float)
        for i in range(0, stream_num):
            data[:, i, :] = self[i].data

        # init pool_new
        from shakecore.core.pool import Pool

        pool_new = []
        for i in range(0, new_stream_num):
            pool_new.append(self[0].copy())
        pool_new = Pool(pool_new)

        # update notes
        for i in range(0, new_stream_num):
            st_1 = win_info[i, 0]
            st_2 = win_info[i, 1]

            win_starttime = self[st_1].stats.starttime
            win_endtime = self[st_2 - 1].stats.endtime
            total_t = 0
            for j in range(st_1, st_2):
                total_t += self[j].stats.starttime - UTCDateTime(0)
            win_mediantime = UTCDateTime(0) + total_t / (st_2 - st_1)
            new_notes = {
                "win_starttime": win_starttime,
                "win_endtime": win_endtime,
                "win_mediantime": win_mediantime,
            }
            new_notes.update(self[i].stats.notes)
            pool_new[i].stats.notes = new_notes
            pool_new[i].stats.starttime = win_starttime

        # initialize pbar
        if flag:
            pbar = tqdm(
                range(0, trace_num),
                desc=f"Stack via {jobs} jobs in CPU",
            )
        else:
            pbar = range(0, trace_num)

        # serial processing
        if jobs == 1:
            for i in pbar:
                result = process_cpu(data[i], method, config, win_info)
                for j in range(0, new_stream_num):
                    pool_new[j].data[i] = result[j]

        # parallel processing
        elif jobs > 1:
            results = Parallel(n_jobs=jobs, backend="loky")(
                delayed(process_cpu)(data[i], method, config, win_info) for i in pbar
            )
            print("assembling results ...", flush=True) if flag else None
            for i, result in enumerate(results):  # trace_num
                for j in range(0, new_stream_num):
                    pool_new[j].data[i] = result[j]
            print("assembling results done", flush=True) if flag else None
        else:
            raise ValueError("'jobs' must be larger than 0.")

        # close pbar
        if flag:
            pbar.close()
    elif device == "cuda":
        process_cuda()
    else:
        raise ValueError(f"Unknown device '{device}'.")

    return pool_new
