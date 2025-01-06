# Purpose: Pick phases for events
# Author: Minzhe Hu
# Date: 2025.1.3
# Email: hmz2018@mail.ustc.edu.cn
import numpy as np
from scipy.stats import kurtosis, skew
from obspy.signal.trigger import classic_sta_lta, trigger_onset
from daspy.basic_tools.preprocessing import normalization


def sta_lta_map(data, fs, sw=0.5, lw=5):
    cft = np.zeros_like(data)
    for ch, d in enumerate(data):
        cft[ch] = classic_sta_lta(d, nsta=round(sw * fs), nlta=round(lw * fs))

    return cft

def kurto_map(data, fs, win=3, diff=True, norm=True):
    nch, nt = data.shape
    w = round(win * fs)
    kts = np.zeros((nch, nt-w))
    for t in range(w, nt):
        kts[:, t - w] = kurtosis(data[:, t - w:t], axis=1)

    pre_nt = w
    if diff:
        kts = np.abs(np.diff(kts, axis=1))
        pre_nt += 1
    if norm:
        kts = normalization(kts)

    kts = np.hstack((np.zeros((nch, pre_nt)), kts))
    return kts

def skew_map(data, fs, win=3, diff=True, norm=True):
    nch, nt = data.shape
    w = round(win * fs)
    kts = np.zeros((nch, nt-w))
    for t in range(w, nt):
        kts[:, t - w] = skew(data[:, t - w:t], axis=1)

    pre_nt = w
    if diff:
        kts = np.abs(np.diff(kts, axis=1))
        pre_nt += 1
    if norm:
        kts = normalization(kts)

    kts = np.hstack((np.zeros((nch, pre_nt)), kts))
    return kts


def map_picking(hot_map, thres1=5, thres2=5, choose_max=True, min_dsp=0):
    pick = []
    amp = []
    for ch, arr in enumerate(hot_map):
        onsets = trigger_onset(arr, thres1=thres1, thres2=thres2)
        if len(onsets) != 0:
            for s, e in onsets:
                if min_dsp > 0:
                    if e - s < min_dsp:
                        continue
                if choose_max:
                    pick.append([ch, np.argmax(arr[s:e+1]) + s])
                    amp.append(np.max(arr[s:e+1]))
                else:
                    pick.append([ch, s])
                    amp.append(arr[s])

    return np.array(pick), np.array(amp)


def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def xcorr(x,y):
    # x is longer than y
    N=len(x)
    M=len(y)
    meany=np.mean(y)
    stdy=np.std(np.asarray(y))
    tmp=rolling_window(x,M)
    c=np.sum((y-meany)*(tmp-np.reshape(np.mean(tmp,-1),(N-M+1,1))),-1)/(M*np.std(tmp,-1)*stdy)
    return c