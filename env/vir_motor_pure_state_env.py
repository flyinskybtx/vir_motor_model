import csv
from datetime import datetime

import gym
import numpy as np
import tqdm

from dige_stl.general_library.math_lib import limit_cycle, anti_clockwise_conv
from dige_stl.general_library.math_macro import CONST
from dige_stl.general_library.signal_generator import SignalGenerator
from virtual_model.vir_model.vir_motor_model import VirRotaryMotorModel
from virtual_model.vir_state_equation.virtual_device_state import VirState


class VirMotorFullStateEnv(gym.Env):
    def __init__(self, u=20, i=4, vel=10, acc=20, noise=0, seq_len=100):
        self.motor = VirRotaryMotorModel()
        self.noise = noise
        self.max_step = seq_len
        self.vel_limit = vel
        self.acc_limit = acc
        self.i_limit = i
        self._step=0

        self.motor.flush()
        self.dt = self.motor.device_data.env_param.dt.value
        self.pn = self.motor.state_equ.motor_data.param.Pn.value
        self.action_space = gym.spaces.Box(-u, u, shape=(2,), dtype=np.float32)
        limits = np.array([i, i, 2 * np.pi / self.pn, vel, acc])
        self.observation_space = gym.spaces.Box(
            low=-limits, high=limits, shape=(5,), dtype=np.float32)

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
        return state, 0, done, info

    def reset(self):
        self._step=0
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


if __name__ == '__main__':
    env = VirMotorFullStateEnv()

    # Dummy run
    _, dummy_state_info = env.reset()  # Ia, Ib, pos, vel acc
    dummy_info = {k + '_0': v for k, v in dummy_state_info.items()}
    _, dummy_new_state_info = env.step(env.action_space.sample())
    dummy_info.update(dummy_new_state_info)
    field_names = list(dummy_info.keys())

    # RUN
    NUM_EPISODES = 2e2
    NUM_STEPS = 5e3

    action = env.action_space.sample()  #

    with open(f"data_same_uaub{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv", 'w', newline='') as csvfile:
        field_names = field_names
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()

        for _ in tqdm.trange(int(NUM_EPISODES)):
            state, state_info = env.reset()  # Ia, Ib, pos, vel acc
            for _ in range(int(NUM_STEPS)):
                info = {k + '_0': v for k, v in state_info.items()}
                new_state, new_state_info = env.step(action)
                # action = env.action_space.sample()  # 每一步的动作
                # s_a_ss = np.concatenate([state, action, new_state]).round(4)
                info.update(new_state_info)

                state_info = {k: new_state_info[k] for k in state_info.keys()}
                writer.writerow(info)
                # state = new_state
