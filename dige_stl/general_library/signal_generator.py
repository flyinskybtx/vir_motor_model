import copy

import numpy as np

from dige_stl.general_library.math_macro import CONST


class SignalType:
    Signal_Type_None = 0
    Signal_Type_Sin = 1
    Signal_Type_Square = 2
    Signal_Type_Triangle = 3
    Signal_Type_Sawtooth = 4
    Signal_Type_Angle = 5
    Signal_Type_RandNorm = 6
    Signal_Type_Const = 7
    Signal_Type_RandUniform = 8


class SignalParam:
    def __init__(self):
        self.fre_hz = 0
        self.amp = 0
        self.offset = 0
        self.signal_type = SignalType.Signal_Type_None


class SignalGenerator:
    def __init__(self):
        self.dt = 0
        self.w = 0
        self.sd = 0
        self.t1 = 1 / 4
        self.t2 = 1 - self.t1
        self.i_nos = 0
        self.param = SignalParam()

    def set_param(self, param: SignalParam, dt):
        self.param = copy.deepcopy(param)
        self.dt = dt
        self.w = CONST.PI * param.fre_hz
        if param.signal_type == SignalType.Signal_Type_Angle:
            self.param.offset = 0

    def get_signal(self):
        self.sd_integral()
        y = 0
        if self.param.signal_type == SignalType.Signal_Type_Sin:
            y = self.param.amp * np.sin(self.sd)
        elif self.param.signal_type == SignalType.Signal_Type_Square:
            y = self.param.amp * np.sign(np.sin(self.sd))
        elif self.param.signal_type == SignalType.Signal_Type_Triangle:
            y = self.param.amp * self.triangle_signal(self.sd * CONST.INV_TWO_PI)
        elif self.param.signal_type == SignalType.Signal_Type_Sawtooth:
            y = self.param.amp * self.sd * CONST.INV_TWO_PI
        elif self.param.signal_type == SignalType.Signal_Type_Angle:
            y = self.sd
        elif self.param.signal_type == SignalType.Signal_Type_RandUniform:
            y = self.param.amp * np.random.uniform(-1, 1)
        elif self.param.signal_type == SignalType.Signal_Type_RandNorm:
            y = self.param.amp * np.random.randn()
        elif self.param.signal_type == SignalType.Signal_Type_Const:
            y = self.param.amp
        else:
            y = 0
        y = y + self.param.offset
        return y

    def sd_integral(self):
        self.sd = self.sd + self.w * self.dt
        if self.sd > CONST.TWO_PI:
            self.sd = self.sd - CONST.TWO_PI
        elif self.sd < 0:
            self.sd = self.sd + CONST.TWO_PI

    def triangle_signal(self, x):
        y = 0
        if x < self.t1:
            y = 4 * x
        elif x < self.t2:
            y = 2 - 4 * x
        elif x < 1:
            y = 4 * x - 4
        else:
            y = 0
        return y
