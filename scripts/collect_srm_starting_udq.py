import argparse
import csv
import os.path
from datetime import datetime

import numpy as np
import tqdm

from data import DATA_DIR
from env.vir_motor_pure_state_env import VirMotorFullStateEnv

argparser = argparse.ArgumentParser(description="PMSM DQ 控制模式的args")
argparser.add_argument('-u', dest='voltage', type=np.float32, default=48, help='电压控制量绝对值的最大值')
argparser.add_argument('-i', dest='current', type=np.float32, default=10, help='状态量电流绝对值的最大值')
argparser.add_argument('-v', dest='vel', type=np.float32, default=1e3, help='状态量速度绝对值的最大值')
argparser.add_argument('-a', dest='acc', type=np.float32, default=1000, help='状态量速度绝对值的最大值')
argparser.add_argument('-n', dest='noise', type=np.float32, default=0.0, help='电流观测的误差级别')
argparser.add_argument('-s', dest='steps', type=int, default=1e4, help='每个episode的最大步数')
argparser.add_argument('-low', dest='u_low', default=0, type=np.float32, help='电压控制低值')
argparser.add_argument('-high', dest='u_high', default=48, type=np.float32, help='电压控制高值')

argparser.add_argument('-N', dest='num_samples', default=1e5, type=np.float32, help='收集的总样本数')


class UdqGenerator:
    def __init__(self, ud_mu, uq_mu, std, decay=0.9):
        self.ud_mu = ud_mu
        self.uq_mu = uq_mu
        self.std = std
        self.decay = decay

    def get_uduq(self):
        ud, uq = np.random.normal(loc=(self.ud_mu, self.uq_mu), scale=(self.std, self.std), size=(2,))
        self.std *= self.decay
        return ud, uq


def get_uduq(low, high, bidirection=False):
    uduq = np.random.uniform(low, high, size=(2,))
    if bidirection:
        uduq = uduq * np.random.choice([-1, 1], size=(2,), replace=True)
    return uduq


if __name__ == '__main__':
    args = argparser.parse_args()
    env = VirMotorFullStateEnv(u=args.voltage, i=args.current, vel=args.vel, acc=args.acc, noise=args.noise,
                               seq_len=args.steps, acc_tol=0.2)

    # Dummy run
    _, dummy_state_info = env.reset()  # Ia, Ib, pos, vel acc
    dummy_info = {k + '_0': v for k, v in dummy_state_info.items()}
    _, _, _, dummy_new_state_info = env.step(env.action_space.sample())
    dummy_info.update(dummy_new_state_info)
    field_names = list(dummy_info.keys())

    # Filename
    filename = f"_{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv"
    filename = '_starting_Udq=' + f'{args.u_low}V-{args.u_high}V' + filename

    if args.noise == 0:
        filename = '_no_noise' + filename
    else:
        filename = f'_{args.noise}_noise' + filename

    filename = f'{int(args.num_samples)}_of' + filename
    filename = os.path.join(DATA_DIR, filename)
    print(f"\nSaving to file: {filename}")

    # RUN
    num_episodes = 0

    # 开始采集
    done = True
    with open(filename, 'w', newline='') as csvfile:
        field_names = field_names
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()

        for _ in tqdm.trange(int(args.num_samples), desc='Collecting:'):
            if done:
                ud, uq = np.random.uniform(args.u_low, args.u_high, size=(2,))
                udq_generator = UdqGenerator(ud, uq, std=1, decay=0.99)
                state, state_info = env.reset(only_step=False, random_state=False)  # 重置step
                num_episodes += 1

            udq = udq_generator.get_uduq()

            info = {k + '_0': v for k, v in state_info.items()}
            new_state, _, done, new_state_info = env.udq_step(udq)
            info.update(new_state_info)

            state_info = {k: new_state_info[k] for k in state_info.keys()}
            writer.writerow(info)

    print(f"Collect {int(args.num_samples)} samples from {num_episodes} episodes.")
