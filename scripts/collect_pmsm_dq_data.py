import argparse
import csv
import os.path
from datetime import datetime

import numpy as np
import tqdm

from data import DATA_DIR
from env.vir_motor_pure_state_env import VirMotorFullStateEnv

argparser = argparse.ArgumentParser(description="PMSM DQ 控制模式的args")
argparser.add_argument('-u', dest='voltage', type=float, default=20, help='电压控制量绝对值的最大值')
argparser.add_argument('-i', dest='current', type=float, default=50, help='状态量电流绝对值的最大值')
argparser.add_argument('-v', dest='vel', type=float, default=100, help='状态量速度绝对值的最大值')
argparser.add_argument('-a', dest='acc', type=float, default=1000, help='状态量速度绝对值的最大值')
argparser.add_argument('-n', dest='noise', type=float, default=0.1, help='电流观测的误差级别')
argparser.add_argument('-s', dest='steps', type=int, default=1e4, help='每个episode的最大步数')
argparser.add_argument('-N', dest='num_samples', default=1e5, type=float, help='收集的总样本数')

if __name__ == '__main__':
    args = argparser.parse_args()
    env = VirMotorFullStateEnv(u=args.voltage, i=args.current, vel=args.vel, acc=args.acc, noise=args.noise,
                               seq_len=args.steps)

    # Dummy run
    _, dummy_state_info = env.reset()  # Ia, Ib, pos, vel acc
    dummy_info = {k + '_0': v for k, v in dummy_state_info.items()}
    _, _, _, dummy_new_state_info = env.step(env.action_space.sample())
    dummy_info.update(dummy_new_state_info)
    field_names = list(dummy_info.keys())

    # Filename
    filename = f"_{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv"
    filename = '_DQ'+filename

    if args.noise == 0:
        filename = 'no_noise' + filename
    else:
        filename = f'{args.noise}_noise' + filename

    filename = f'{int(args.num_samples)}_of_' + filename
    filename = os.path.join(DATA_DIR, filename)
    print(f"Saving to file: {filename}")

    # RUN
    done = True
    num_episodes = 0
    state, state_info = env.reset()  # Ia, Ib, pos, vel acc

    with open(filename, 'w', newline='') as csvfile:
        field_names = field_names
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()

        for _ in tqdm.trange(int(args.num_samples), desc='Collecting:'):
            if done:
                # todo: 现在的电压是给的随机的，在0值附近的时候速度收敛缓慢
                du, dq = np.random.uniform(-args.voltage, args.voltage, size=(2,))
                env.reset(only_step=True)  # 重置step
                num_episodes += 1

            info = {k + '_0': v for k, v in state_info.items()}
            dudq = (du, dq)
            new_state, _, done, new_state_info = env.udq_step(dudq)
            info.update(new_state_info)

            state_info = {k: new_state_info[k] for k in state_info.keys()}
            writer.writerow(info)

    print(f"Collect {int(args.num_samples)} samples from {num_episodes} episodes.")
