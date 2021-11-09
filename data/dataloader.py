import os.path
from glob import glob

import numpy as np

from data import DATA_DIR


class AllData(dict):
    def extend(self, dd):
        for k, v in dd.items():
            if k in self.keys():
                self.update({k: np.concatenate([self.get(k), v], axis=0)})
            else:
                self.__setitem__(k, v)


def load_dir(dirname):
    data = dict()
    for filename in glob(dirname + "/*.npy"):
        item_name = os.path.basename(filename).strip('.npy')
        data[item_name] = np.load(filename)
    return data


if __name__ == '__main__':
    all_data = AllData()
    for dirname in glob(DATA_DIR + '/*'):
        data = load_dir(dirname)
        all_data.extend(data)

        for k, v in all_data.items():
            print(f'{k}:{np.shape(v)}')
