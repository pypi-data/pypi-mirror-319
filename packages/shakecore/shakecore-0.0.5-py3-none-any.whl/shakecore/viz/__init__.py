from shakecore.core.utils import FunctionDescriptor

from .dayplot import dayplot
from .fk import fk
from .fplot import fplot
from .fwaterfall import fwaterfall
from .geometry import geometry
from .plot import plot
from .radon import radon
from .singleplot import singleplot
from .spectrogram import spectrogram
from .waterfall import waterfall


class Viz:
    def __init__(self, instance):
        self.instance = instance

    fk = FunctionDescriptor(fk)
    plot = FunctionDescriptor(plot)
    fplot = FunctionDescriptor(fplot)
    radon = FunctionDescriptor(radon)
    dayplot = FunctionDescriptor(dayplot)
    singleplot = FunctionDescriptor(singleplot)
    waterfall = FunctionDescriptor(waterfall)
    fwaterfall = FunctionDescriptor(fwaterfall)
    spectrogram = FunctionDescriptor(spectrogram)
    geometry = FunctionDescriptor(geometry)
