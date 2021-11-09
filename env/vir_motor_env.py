import csv
from datetime import datetime

import gym
import numpy as np
import tqdm

from dige_stl.general_library.math_lib import limit_cycle, anti_clockwise_conv
from virtual_model.vir_model.vir_motor_model import VirRotaryMotorModel
from virtual_model.vir_state_equation.virtual_device_state import VirState


class VirMotorEnv(gym.Env):
    def __init__(self, Ia=4, Ib=4, vel=10, acc=20):
        self.motor = VirRotaryMotorModel()
        self.motor.flush()
        self.dt = self.motor.device_data.env_param.dt.value
        self.pn = self.motor.state_equ.motor_data.param.Pn.value
        self.action_space = gym.spaces.Box(-20, 20, shape=(2,), dtype=np.float32)
        limits = np.array([Ia, Ib, 2 * np.pi / self.pn, vel, acc])
        self.observation_space = gym.spaces.Box(
            low=-limits, high=limits, shape=(5,), dtype=np.float32)

    def step(self, action):
        ua, ub = action
        motor_input = self.motor.device_data.motor.input
        motor_input.Ua.value = ua
        motor_input.Ub.value = ub
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

        state = np.array([Ia, Ib, pos, vel, acc])
        return state

    def reset(self):
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

        state = np.array([Ia, Ib, pos, vel, acc])
        return state

    def render(self, mode="human"):
        pass


if __name__ == '__main__':
    NUM_EPISODES = 1e2
    NUM_STEPS = 5e2
    
    env = VirMotorEnv()

    samples = []
    with open(f"data_ {datetime.now().strftime('%Y%m%d-%H%M%S')}.csv", 'w', newline='') as csvfile:
        field_names = ['Ia', 'Ib', 'pos', 'vel', 'acc', 'Ua', 'Ub', 'Ia_', 'Ib_', 'pos_', 'vel_', 'acc_']
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()

        action = env.action_space.sample() #

        for _ in tqdm.trange(int(NUM_EPISODES)):
            state = env.reset()  # Ia, Ib, pos, vel acc
            for _ in range(int(NUM_STEPS)):
                new_state = env.step(action)
                # action = env.action_space.sample()  # 每一步的动作
                s_a_ss = np.concatenate([state, action, new_state]).round(4)
                writer.writerow({k: v for k, v in zip(field_names, s_a_ss)})
                state = new_state
