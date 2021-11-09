import copy
import numpy as np

from virtual_model.vir_state_equation.virtual_device_state import VirState


def static_friction(f_driving, f_static):
    if f_driving > f_static:
        f_driving = f_driving - f_static
    elif f_driving < -f_static:
        f_driving = f_driving + f_static
    else:
        f_driving = 0
    return f_driving


class DynamicEquation:  # 直线电机和旋转电机统一。
    def __init__(self):
        self.m = 0
        self.m_inv = 0
        self.fric = 0
        self.fric_direction = 0
        self.damp = 0

    def flush(self, mass, fric, damp):  # 需要根据模型得到等价参数
        self.m = mass
        self.fric = fric
        self.damp = damp
        if self.m == 0:
            self.m_inv = 0
        else:
            self.m_inv = 1/self.m

    def set_friction_direction(self, vel):
        self.fric_direction = np.sign(vel)

    def running(self, state: VirState, f):
        f_in = copy.deepcopy(f)
        f -= self.damp*state.vel
        if self.fric_direction == 0:
            f = static_friction(f, self.fric)
        elif self.fric_direction > 0:
            f -= self.fric
        else:
            f += self.fric
        fd = f_in - f
        acc = f*self.m_inv
        return acc

