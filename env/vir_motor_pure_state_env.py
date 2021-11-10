import csv
from datetime import datetime

import gym
import numpy as np
import tqdm

from dige_stl.general_library.math_lib import limit_cycle, anti_clockwise_conv, clockwise_conv
from dige_stl.general_library.math_macro import CONST
from virtual_model.vir_model.vir_motor_model import VirRotaryMotorModel
from virtual_model.vir_state_equation.virtual_device_state import VirState


class VirMotorFullStateEnv(gym.Env):
    def __init__(self, u=20, i=50, vel=100, acc=1000, noise=0, seq_len=1e4):
        self.motor = VirRotaryMotorModel()
        self.noise = noise
        self.max_step = int(seq_len)
        self.vel_limit = vel
        self.acc_limit = acc
        self.i_limit = i
        self._step = 0

        self.motor.flush()
        self.dt = self.motor.device_data.env_param.dt.value
        self.pn = self.motor.state_equ.motor_data.param.Pn.value
        self.action_space = gym.spaces.Box(-u, u, shape=(2,), dtype=np.float32)
        limits = np.array([i, i, 2 * np.pi / self.pn, vel, acc])
        self.observation_space = gym.spaces.Box(
            low=-limits, high=limits, shape=(5,), dtype=np.float32)

    def udq_step(self, uduq):
        ud, uq = uduq
        pos = self.motor.device_data.motor.output.pos.value
        angle_e = pos * self.pn
        angle_e = limit_cycle(angle_e, CONST.TWO_PI)  # 限制在0~2pi之间
        ua, ub = clockwise_conv(angle_e, ud, uq)
        return self.step((ua, ub))


    def step(self, action):
        ua, ub = action
        motor_input = self.motor.device_data.motor.input
        motor_input.Ua.value = ua
        motor_input.Ub.value = ub
        motor_input.enable.value = 1
        pos = self.motor.device_data.motor.output.pos.value
        angle_e = pos * self.pn
        angle_e = limit_cycle(angle_e, CONST.TWO_PI)  # 限制在0~2pi之间
        Ud, Uq = anti_clockwise_conv(angle_e, ua, ub)

        self.motor.running()
        output = self.motor.device_data.motor.output
        Ia = output.Ia.value
        Ib = output.Ib.value
        pos = output.pos.value
        vel = output.vel.value
        acc = output.acc.value
        Id = output.Id.value
        Iq = output.Iq.value

        if any(np.abs(np.array([Ia, Ib, vel, acc, self._step])) > np.array([self.i_limit, self.i_limit, self.vel_limit,
                                                                            self.acc_limit, self.max_step])):
            done = True
        else:
            done = False

        state = np.array([Ia, Ib, pos, vel, acc])
        info = {}
        for vv in ['Ia', 'Ib', 'pos', 'vel', 'acc', 'Id', 'Iq', 'Ud', 'Uq']:
            info[vv] = eval(vv)
        self._step += 1
        return state, 0, done, info

    def reset(self):
        self._step = 0
        self.motor.flush()
        vir_state = VirState()
        Ia, Ib, pos, vel, acc = self.observation_space.sample()
        vir_state.pos = pos
        vir_state.vel = vel
        vir_state.acc = acc
        angle_e = pos * self.pn
        angle_e = limit_cycle(angle_e, 2 * np.pi)  # 限制在0~2pi之间
        Id, Iq = anti_clockwise_conv(angle_e, Ia, Ib)
        vir_state.Id = Id
        vir_state.Iq = Iq
        self.motor.state_equ.state = vir_state

        motor_input = self.motor.device_data.motor.input
        motor_input.enable.value = 1
        self.motor.running()

        output = self.motor.device_data.motor.output
        Ia = output.Ia.value
        Ib = output.Ib.value
        pos = output.pos.value
        vel = output.vel.value
        acc = output.acc.value
        Id = output.Id.value
        Iq = output.Iq.value

        if self.noise != 0:
            Ia *= (1 + self.noise * np.random.randn())
            Ib *= (1 + self.noise * np.random.randn())

        info = {}
        for vv in ['Ia', 'Ib', 'pos', 'vel', 'acc', 'Id', 'Iq']:
            info[vv] = eval(vv)
        state = np.array([Ia, Ib, pos, vel, acc])
        return state, info

    def render(self, mode="human"):
        pass
