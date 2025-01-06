# Purpose: Finding the source of the fault scattered waves from the waveforms recorded by DAS
# Author: Minzhe Hu
# Date: 2023.8.27
# Email: hmz2018@mail.ustc.edu.cn
import multiprocessing
import numpy as np
from math import ceil
from daspy.advanced_tools.decomposition import fk_filter


def csb_stacking(data, lent, slope):
    """
    Use coherence- and symmetry-based method to stack scattered wave from 1
    channel location.
    """
    nx, nt = data.shape
    nv = len(slope)
    lenx = int((nx - 1) / 2)
    t_ex = lent + ceil(lenx * max(slope))
    data = np.hstack((data, np.zeros((nx, t_ex))))

    intensity = np.zeros(nt)
    for i in range(nt):
        left = np.zeros((nv, lent))
        right = np.zeros((nv, lent))
        for j, s in enumerate(slope):
            for k in range(lenx + 1):
                start = i + round(k * s)
                left[j] += data[lenx - k, start:start + lent]
                right[j] += data[lenx + k, start:start + lent]
        intensity[i] = np.sum(abs(left * right)**2, axis=1).max()
    return intensity


def csb_stacking_rapid(data, slope):
    """
    Use coherence- and symmetry-based method to stack scattered wave from 1
    channel location.
    """
    nx, nt = data.shape
    nv = len(slope)
    lenx = int((nx - 1) / 2)
    t_ex = ceil(lenx * max(slope))
    data = np.hstack((data, np.zeros((nx, t_ex))))

    left = np.zeros((nv, nt))
    right = np.zeros((nv, nt))
    for j, s in enumerate(slope):
        for k in range(lenx + 1):
            start = round(k * s)
            left[j] += data[lenx - k, start:start + nt]
            right[j] += data[lenx + k, start:start + nt]

    return np.sum(abs(left * right)**2, axis=1).max()


def fault_detection(data, dx, fs, winx=200, wint=1, vmin=200, vmax=700, nv=30,
                    fk=True, rapid=False):
    """
    Obtain the spatiotemporal distribution of scattering intensity and velocity
    from the waveform.
    """
    if isinstance(fk, dict):
        fk.setdefault('vmin', vmin)
        fk.setdefault('vmax', vmax)
        data = fk_filter(data, dx, fs, mode='retain', **fk)
    elif fk:
        data = fk_filter(data, dx, fs, vmin=vmin, vmax=vmax, edge=0.15,
                         mode='retain')


    nx, nt = data.shape
    lenx = round(winx / dx)
    lent = round(wint * fs)
    data = np.r_[np.zeros((lenx, nt)), data, np.zeros((lenx, nt))]

    cores = multiprocessing.cpu_count() - 1
    pool = multiprocessing.Pool(processes=cores)

    slope = 1 / np.linspace(vmin, vmax, nv) * dx * fs
    tasks = []
    if rapid:
        for i in range(nx): 
            tasks.append((data[i:i + 2 * lenx + 1], slope))
        intensity = np.array(pool.starmap(csb_stacking_rapid, tasks))
    else:
        for i in range(nx):
            tasks.append((data[i:i + 2 * lenx + 1], lent, slope))
        intensity = np.array(pool.starmap(csb_stacking, tasks))
    return intensity
