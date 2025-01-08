import warnings

import numpy as np
import scipy
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter, laplace, median_filter, uniform_filter

try:
    import cupy as cp
    import cupyx

    GUDA_MODE = True
except Exception:
    GUDA_MODE = False


def bandpass_cpu(data, freqmin, freqmax, df, corners=4, zerophase=False):
    fe = 0.5 * df
    low = freqmin / fe
    high = freqmax / fe
    # raise for some bad scenarios
    if high - 1.0 > -1e-6:
        msg = (
            "Selected high corner frequency ({}) of bandpass is at or "
            "above Nyquist ({}). Applying a high-pass instead."
        ).format(freqmax, fe)
        warnings.warn(msg)
        return highpass_cpu(
            data, freq=freqmin, df=df, corners=corners, zerophase=zerophase
        )
    if low > 1:
        msg = "Selected low corner frequency is above Nyquist."
        raise ValueError(msg)
    z, p, k = scipy.signal.iirfilter(
        corners, [low, high], btype="band", ftype="butter", output="zpk"
    )
    sos = scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = scipy.signal.sosfilt(sos, data, axis=1)
        out = scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def bandpass_cuda(data, freqmin, freqmax, df, corners=4, zerophase=False):
    fe = 0.5 * df
    low = freqmin / fe
    high = freqmax / fe
    # raise for some bad scenarios
    if high - 1.0 > -1e-6:
        msg = (
            "Selected high corner frequency ({}) of bandpass is at or "
            "above Nyquist ({}). Applying a high-pass instead."
        ).format(freqmax, fe)
        warnings.warn(msg)
        return highpass_cuda(
            data, freq=freqmin, df=df, corners=corners, zerophase=zerophase
        )
    if low > 1:
        msg = "Selected low corner frequency is above Nyquist."
        raise ValueError(msg)
    z, p, k = cupyx.scipy.signal.iirfilter(
        corners, [low, high], btype="band", ftype="butter", output="zpk"
    )
    sos = cupyx.scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        out = cupyx.scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = cupyx.scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def bandstop_cpu(data, freqmin, freqmax, df, corners=4, zerophase=False):
    fe = 0.5 * df
    low = freqmin / fe
    high = freqmax / fe
    # raise for some bad scenarios
    if high > 1:
        high = 1.0
        msg = (
            "Selected high corner frequency is above Nyquist. "
            + "Setting Nyquist as high corner."
        )
        warnings.warn(msg)
    if low > 1:
        msg = "Selected low corner frequency is above Nyquist."
        raise ValueError(msg)
    z, p, k = scipy.signal.iirfilter(
        corners, [low, high], btype="bandstop", ftype="butter", output="zpk"
    )
    sos = scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = scipy.signal.sosfilt(sos, data, axis=1)
        out = scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def bandstop_cuda(data, freqmin, freqmax, df, corners=4, zerophase=False):
    fe = 0.5 * df
    low = freqmin / fe
    high = freqmax / fe
    # raise for some bad scenarios
    if high > 1:
        high = 1.0
        msg = (
            "Selected high corner frequency is above Nyquist. "
            + "Setting Nyquist as high corner."
        )
        warnings.warn(msg)
    if low > 1:
        msg = "Selected low corner frequency is above Nyquist."
        raise ValueError(msg)
    z, p, k = cupyx.scipy.signal.iirfilter(
        corners, [low, high], btype="bandstop", ftype="butter", output="zpk"
    )
    sos = cupyx.scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        out = cupyx.scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = cupyx.scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def lowpass_cpu(data, freq, df, corners=4, zerophase=False):
    fe = 0.5 * df
    f = freq / fe
    # raise for some bad scenarios
    if f > 1:
        f = 1.0
        msg = (
            "Selected corner frequency is above Nyquist. "
            + "Setting Nyquist as high corner."
        )
        warnings.warn(msg)
    z, p, k = scipy.signal.iirfilter(
        corners, f, btype="lowpass", ftype="butter", output="zpk"
    )
    sos = scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = scipy.signal.sosfilt(sos, data, axis=1)
        out = scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def lowpass_cuda(data, freq, df, corners=4, zerophase=False):
    fe = 0.5 * df
    f = freq / fe
    # raise for some bad scenarios
    if f > 1:
        f = 1.0
        msg = (
            "Selected corner frequency is above Nyquist. "
            + "Setting Nyquist as high corner."
        )
        warnings.warn(msg)
    z, p, k = cupyx.scipy.signal.iirfilter(
        corners, f, btype="lowpass", ftype="butter", output="zpk"
    )
    sos = cupyx.scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        out = cupyx.scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = cupyx.scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def highpass_cpu(data, freq, df, corners=4, zerophase=False):
    fe = 0.5 * df
    f = freq / fe
    # raise for some bad scenarios
    if f > 1:
        msg = "Selected corner frequency is above Nyquist."
        raise ValueError(msg)
    z, p, k = scipy.signal.iirfilter(
        corners, f, btype="highpass", ftype="butter", output="zpk"
    )
    sos = scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = scipy.signal.sosfilt(sos, data, axis=1)
        out = scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def highpass_cuda(data, freq, df, corners=4, zerophase=False):
    fe = 0.5 * df
    f = freq / fe
    # raise for some bad scenarios
    if f > 1:
        msg = "Selected corner frequency is above Nyquist."
        raise ValueError(msg)
    z, p, k = cupyx.scipy.signal.iirfilter(
        corners, f, btype="highpass", ftype="butter", output="zpk"
    )
    sos = cupyx.scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        out = cupyx.scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = cupyx.scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def common_mode_cpu(data, traces=[None, None], method="median"):
    tr1, tr2 = traces
    if tr1 is None:
        tr1 = 0
    if tr2 is None:
        tr2 = data.shape[0]

    if method == "median":
        common = np.median(data[tr1:tr2, :], axis=0, keepdims=True)
    elif method == "mean":
        common = np.mean(data[tr1:tr2, :], axis=0, keepdims=True)

    xx = np.sum(common**2)
    if xx != 0:
        for i in range(tr1, tr2):
            xc = np.sum(data[i, :] * common)
            data[i, :] = data[i, :] - xc / xx * common

    return data


def common_mode_cuda(data, traces=[None, None]):
    tr1, tr2 = traces
    if tr1 is None:
        tr1 = 0
    if tr2 is None:
        tr2 = data.shape[0]

    common = cp.median(data[tr1:tr2, :], axis=0, keepdims=True)

    xx = cp.sum(common**2)
    for i in range(tr1, tr2 + 1):
        xc = cp.sum(data[i, :] * common)
        data[i, :] = data[i, :] - xc / xx * common

    return data


def spike_cpu(data, kernel_size=(10, 5), threshold=10, fill_value=None):
    absdata = np.abs(data)
    n_trace, npts = kernel_size

    # median filter
    median1 = median_filter(absdata, size=(n_trace, 1))
    median2 = median_filter(median1, size=(1, npts))
    ratio = absdata / median2

    # threshold
    row, col = np.where(ratio > threshold)

    # interpolate
    if fill_value is None:
        for j in set(col):
            bad_trace = row[col == j]
            good_trace = list(set(range(len(data))) - set(bad_trace))
            f = interp1d(
                good_trace,
                data[good_trace, j],
                bounds_error=False,
                fill_value=(data[good_trace[0], j], data[good_trace[-1], j]),
            )
            data[bad_trace, j] = f(bad_trace)
    else:
        for j in set(col):
            bad_trace = row[col == j]
            good_trace = list(set(range(len(data))) - set(bad_trace))
            data[bad_trace, j] = fill_value

    return data


def spike_cuda(data, kernel_size=(10, 5), threshold=10, fill_value=None):
    absdata = cp.abs(data)
    n_trace, npts = kernel_size

    # median filter
    median1 = cp.ndimage.median_filter(absdata, size=(n_trace, 1))
    median2 = cp.ndimage.median_filter(median1, size=(1, npts))
    ratio = absdata / median2

    # threshold
    row, col = cp.where(ratio > threshold)

    # interpolate
    if fill_value is None:
        for j in set(col):
            bad_trace = row[col == j]
            good_trace = list(set(range(len(data))) - set(bad_trace))
            f = interp1d(
                good_trace,
                data[good_trace, j],
                bounds_error=False,
                fill_value=(data[good_trace[0], j], data[good_trace[-1], j]),
            )
            data[bad_trace, j] = f(bad_trace)
    else:
        for j in set(col):
            bad_trace = row[col == j]
            good_trace = list(set(range(len(data))) - set(bad_trace))
            data[bad_trace, j] = fill_value

    return data


def medfilt_cpu(data, kernel_size=(10, 5)):
    return median_filter(data, size=kernel_size)


def medfilt_cuda(data, kernel_size=(10, 5)):
    return cp.ndimage.median_filter(data, size=kernel_size)


def uniform_cpu(data, kernel_size=(10, 5)):
    return uniform_filter(data, size=kernel_size)


def uniform_cuda(data, kernel_size=(10, 5)):
    return cp.ndimage.uniform_filter(data, size=kernel_size)


def gaussian_cpu(data, sigma=1):
    return gaussian_filter(data, sigma=sigma)


def gaussian_cuda(data, sigma=1):
    return cp.ndimage.gaussian_filter(data, sigma=sigma)


def laplace_cpu(data):
    return laplace(data)


def laplace_cuda(data):
    return cp.ndimage.laplace(data)


def svd_cpu(data, threshold=0.5):
    # threshold is a percentage of the maximum singular value
    U, s, V = np.linalg.svd(data, full_matrices=False)
    max_s = np.max(s)
    s[s < threshold * max_s] = 0
    return np.dot(U, np.dot(np.diag(s), V))


def svd_cuda(data, threshold=0.5):
    # threshold is a percentage of the maximum singular value
    U, s, V = cp.linalg.svd(data, full_matrices=False)
    max_s = cp.max(s)
    s[s < threshold * max_s] = 0
    return cp.dot(U, cp.dot(cp.diag(s), V))


def wiener_cpu(data, kernel_size=(10, 5), noise=None):
    return scipy.signal.wiener(data, mysize=kernel_size, noise=noise)


def wiener_cuda(data, kernel_size=(10, 5), noise=None):
    return cupyx.scipy.signal.wiener(data, mysize=kernel_size, noise=noise)


def lowpass_cheby_2_cpu(data, freq, df, maxorder=12, ba=False, freq_passband=False):
    nyquist = df * 0.5
    # rp - maximum ripple of passband, rs - attenuation of stopband
    rp, rs, order = 1, 96, 1e99
    ws = freq / nyquist  # stop band frequency
    wp = ws  # pass band frequency
    # raise for some bad scenarios
    if ws > 1:
        ws = 1.0
        msg = (
            "Selected corner frequency is above Nyquist. "
            + "Setting Nyquist as high corner."
        )
        warnings.warn(msg)
    while True:
        if order <= maxorder:
            break
        wp = wp * 0.99
        order, wn = scipy.signal.cheb2ord(wp, ws, rp, rs, analog=0)
    if ba:
        out = scipy.signal.cheby2(order, rs, wn, btype="low", analog=0, output="ba")
        return out.astype(data.dtype)
    sos = scipy.signal.cheby2(order, rs, wn, btype="low", analog=0, output="sos")
    if freq_passband:
        out = scipy.signal.sosfilt(sos, data, axis=1), wp * nyquist
        return out.astype(data.dtype)
    out = scipy.signal.sosfilt(sos, data, axis=1)
    return out.astype(data.dtype)


def lowpass_cheby_2_cuda(data, freq, df, maxorder=12, ba=False, freq_passband=False):
    nyquist = df * 0.5
    # rp - maximum ripple of passband, rs - attenuation of stopband
    rp, rs, order = 1, 96, 1e99
    ws = freq / nyquist  # stop band frequency
    wp = ws  # pass band frequency
    # raise for some bad scenarios
    if ws > 1:
        ws = 1.0
        msg = (
            "Selected corner frequency is above Nyquist. "
            + "Setting Nyquist as high corner."
        )
        warnings.warn(msg)
    while True:
        if order <= maxorder:
            break
        wp = wp * 0.99
        order, wn = cupyx.scipy.signal.cheb2ord(wp, ws, rp, rs, analog=0)
    if ba:
        out = cupyx.scipy.signal.cheby2(
            order, rs, wn, btype="low", analog=0, output="ba"
        )
        return out.astype(data.dtype)
    sos = cupyx.scipy.signal.cheby2(order, rs, wn, btype="low", analog=0, output="sos")
    if freq_passband:
        out = cupyx.scipy.signal.sosfilt(sos, data, axis=1), wp * nyquist
        return out.astype(data.dtype)
    out = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
    return out.astype(data.dtype)
