import numpy as np
from collections.abc import Iterable
from tqdm import tqdm
import daspy.basic_tools.visualization as DBV
from daspy.core import Section, DASDateTime
from daspy.seismic_detection.phase_picking import *


def plot(data, obj='waveform', title=None, cmap=None, vmax=None, vmin=None,
         **kwargs):
    if obj == 'pickmap':
        cmap = 'hot' if cmap is None else cmap
        vmax = np.percentile(abs(data), 99) if vmax is None else vmax
        vmin = np.percentile(abs(data), 80) if vmin is None else vmin
        title = obj
        obj = 'waveform'

    return DBV.plot(data, title=title, cmap=cmap, vmin=vmin, vmax=vmax,
                    **kwargs)

class DetectSection(Section):

    def __str__(self):
        describe = ''
        n = max(map(len, self.__dict__.keys()))
        for key, value in self.__dict__.items():
            if key in ['data', 'geometry', 'pickmap']:
                describe = '{}: shape{}\n'.format(key.rjust(n), value.shape) \
                    + describe
            elif key in ['dx', 'start_distance', 'gauge_length']:
                describe += '{}: {} m\n'.format(key.rjust(n), value)
            elif key == 'fs':
                describe += '{}: {} Hz\n'.format(key.rjust(n), value)
            elif key == 'start_time':
                if isinstance(value, DASDateTime):
                    describe += '{}: {}\n'.format(key.rjust(n), value)
                else:
                    describe += '{}: {} s\n'.format(key.rjust(n), value)
            elif key == 'pick':
                describe += '{}: {}\n'.format(key.rjust(n), len(value))
            else:
                describe += '{}: {}\n'.format(key.rjust(n), value)
        return describe
    
    __repr__ = __str__

    def plot(self, obj='waveform', kwargs_pro={}, **kwargs):
        if obj == 'pickmap':
            if 'data' not in kwargs.keys():
                if not hasattr(self, 'pickmap') or len(kwargs_pro):
                    self.calc_pickmap(**kwargs_pro)
                kwargs['data']= self.pickmap
            kwargs.setdefault('cmap', 'hot')
            kwargs.setdefault('vmax', np.percentile(abs(kwargs['data']), 99.9))
            kwargs.setdefault('vmin', np.percentile(abs(kwargs['data']), 95))
            kwargs.setdefault('title', obj)
            obj = 'waveform'
        elif obj == 'phasepick':
            if 'data' not in kwargs.keys():
                kwargs['data']= self.data
            if 'pick' not in kwargs.keys():
                if not hasattr(self, 'pick') or len(kwargs_pro):
                    self.map_picking(**kwargs_pro)
                kwargs['pick'] = self.pick
                if len(kwargs['pick']):
                    kwargs['pick'][:, 0] -= self.start_channel

        super().plot(obj=obj, kwargs_pro=kwargs_pro, **kwargs)

    def calc_pickmap(self, method='sta_lta', **kwargs):
        if isinstance(method, str):
            method = [method]
        self.pickmap = np.zeros_like(self.data)
        for m in method:
            if m == 'sta_lta':
                self.pickmap += sta_lta_map(self.data, self.fs, **kwargs)
            elif m == 'kurto':
                self.pickmap += kurto_map(self.data, self.fs, **kwargs)
            elif m == 'skew':
                self.pickmap += skew_map(self.data, self.fs, **kwargs)

        return self.pickmap

    def map_picking(self, thres1=5, thres2=5, choose_max=False, min_dt=0,
                    **kwargs):
        if not hasattr(self, 'pickmap') or len(kwargs):
            self.calc_pickmap(**kwargs)

        pick, amp = map_picking(self.pickmap, thres1=thres1, thres2=thres2,
                                choose_max=choose_max,
                                min_dsp=min_dt*self.fs).astype(float)
        if len(pick):
            pick[:, 0] += self.start_channel
            pick[:, 1] = pick[:, 1] / self.fs

        self.pick = pick
        self.pick_amp = amp
        return pick

    def symmetry_detection(self, win=5000):
            sec = self.copy()
            sec.normalization()
            win_ch = round(win / self.dx)
            cc = np.zeros(self.nch)
            for sch in range(self.nch):
                win_ch_use = min(win_ch, sch, sec.nch-sch-1)
                if win_ch_use > 0:
                    panel1 = sec.data[sch-win_ch_use:sch]
                    panel1 = panel1[::-1]
                    panel2 = sec.data[sch+1:sch+win_ch_use+1]
                    cc[sch] = np.sum(panel1 * panel2) / win_ch
            self.signal_channel = self.start_channel + np.argmax(cc)
            return cc / sec.nt


    def trimming_pick(self, pick, t_win=0.5):
        sp = round(t_win * self.fs)
        if isinstance(pick, Iterable):
            if len(pick) != self.nch:
                raise ValueError('Length of pick should equals to channel '
                                 'number.')
            if isinstance(pick[0], DASDateTime):
                pick = [p - self.start_time for p in pick]
            pick = np.round(np.array(pick) * self.fs).astype(int)
            data = np.zeros((self.nch, 2 * sp))
            for i, p in enumerate(pick):
                data[i] = self.data[i, p-sp:p+sp]
            self.data = data
            self.start_time = -t_win
        else:
            self.trimming(tmin=pick-t_win, tmax=pick+t_win)
        return self


    def relative_arrival(self, pick, t_win=0.5, dch=30, dt_max=0.1, thresh=0,
                         positive=True, weight_pow=1):
        dsp_max = round(dt_max * self.fs)
        sec_win1 = self.copy()
        sec_win2 = self.copy()
        sec_win1.trimming_pick(pick, t_win=t_win)
        sec_win2.trimming_pick(pick, t_win=t_win+dt_max)
        G = []
        d = []
        for i in tqdm(range(self.nch)):
            for j in range(1, dch+1):
                if i+j >= self.nch:
                    continue
                cc = xcorr(sec_win2.data[i], sec_win1.data[i+j])
                if not positive:
                    cc = np.abs(cc)
                w = max(cc)
                if w < thresh:
                    continue
                w = w ** weight_pow
                d.append((np.argmax(cc) - dsp_max) * w)
                Gl = np.zeros(self.nch-1)
                Gl[i:i+j] = w
                G.append(Gl)

        G = np.array(G)
        idx = np.where(np.sum(G, axis=0) > 0)[0]
        print(len(idx))
        G = np.mat(G[:, idx])
        print(G.shape)
        d = np.mat(d).T
        try:
            m = (G.T * G).I * G.T * d
        except:
            m = G.I * d
            print('xxx')
        time_shift_difference = np.zeros(self.nch - 1)
        time_shift_difference[idx] = np.array(m)[:,0]
        time_shift = np.cumsum(time_shift_difference) / self.fs
        time_shift = np.insert(time_shift, 0, 0)
        if isinstance(pick, Iterable):
            if isinstance(pick[0], DASDateTime):
                pick = [p - self.start_time for p in pick]

        return - time_shift + np.array(pick)


    @classmethod
    def from_section(clc, raw_sec):
        raw_dict = raw_sec.__dict__
        data = raw_dict.pop('data')
        return clc(data, **raw_dict)