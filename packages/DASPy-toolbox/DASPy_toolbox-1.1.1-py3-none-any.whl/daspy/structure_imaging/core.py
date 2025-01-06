import matplotlib.pyplot as plt
from daspy.core import Section
from daspy.structure_imaging.fault_zone import fault_detection
from daspy.seismic_detection.phase_picking import *



class ImagingSection(Section):

    def plot(self, obj='waveform', kwargs_pro={}, **kwargs):
        if obj == 'fault':
            kwargs.setdefault('data', self.scattering_intensity)
            if kwargs['data'].ndim == 1:
                plt.plot(kwargs['data'])
                plt.show()
                return None
            kwargs.setdefault('cmap', 'hot')
            kwargs.setdefault('vmax', np.percentile(kwargs['data'], 80))
            kwargs.setdefault('vmin', np.percentile(kwargs['data'], 20))
            kwargs.setdefault('title', obj)
            kwargs.setdefault('colorbar_label', 'scattering intensity')
            obj = 'waveform'

        super().plot(obj=obj, kwargs_pro=kwargs_pro, **kwargs)

    def fault_detection(self, winx=200, wint=1, vmin=200, vmax=700, nv=30,
                        fk=True, rapid=False):

        intensity = fault_detection(self.data, self.dx, self.fs, winx=winx,
                                    wint=wint, vmin=vmin, vmax=vmax, nv=nv,
                                    fk=fk, rapid=rapid)
        self.scattering_intensity = intensity
        return intensity

    @classmethod
    def from_section(clc, raw_sec):
        raw_dict = raw_sec.__dict__
        data = raw_dict.pop('data')
        return clc(data, **raw_dict)