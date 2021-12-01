import datetime
import os.path
import re

import tensorflow as tf

from data import DATA_DIR
from train.models import MODEL_DIR
from train.results import RESULT_DIR
from train.tb_logs import LOG_DIR

import numpy as np
import pandas as pd


# In[2]:

def train_on_data(filename, dq=True):
    data_name = filename.split(os.sep)[-1].split('.csv')[0]
    data_name = re.sub('=', '_', data_name)
    print(f"Working on dataset: {data_name}")

    df = pd.read_csv(filename)
    names = [
        'Id_0', 'Iq_0', 'vel_0', 'vel', 'Id', 'Iq', 'Ud', 'Uq', 'Ia', 'Ib', 'Ia_0',
        'Ib_0', 'Ua', 'Ub', 'pos_0', 'pos'
    ]
    Id_0, Iq_0, vel_0, vel, Id, Iq, Ud, Uq, Ia, Ib, Ia_0, Ib_0, Ua, Ub, pos_0, pos = [
        df[name] for name in names
    ]

    if dq:
        train_X = np.stack([Id_0, Iq_0, vel_0, Ud, Uq], axis=-1)
        train_Y = np.stack([Id, Iq, vel], axis=-1)
        tb_log_dir = os.path.join(LOG_DIR, 'sim_dq', data_name)
    else:
        train_X = np.stack([Ia_0, Ib_0, pos_0, vel_0, Ua, Ub], axis=-1)
        train_Y = np.stack([Ia, Ib, vel], axis=-1)
        tb_log_dir = os.path.join(LOG_DIR, 'sim_ab', data_name)

    print(f"Train data size: {train_X.shape}->{train_Y.shape}")

    ## -------------------------
    model = tf.keras.models.Sequential(name='mlp_' + data_name)
    model.add(tf.keras.layers.Input(train_X.shape[-1], ))
    model.add(tf.keras.layers.Dense(128, activation='relu'))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dense(train_Y.shape[-1], activation='linear'))
    model.summary()

    if dq:
        model_h5 = os.path.join(MODEL_DIR, data_name+'_dq.h5')
    else:
        model_h5 = os.path.join(MODEL_DIR, data_name+'_ab.h5')

    if os.path.exists(model_h5):
        model.load_weights(model_h5)
        print("Load from trained model.\n")

    model.compile(loss=tf.keras.losses.MSE, optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4))

    model.fit(train_X, train_Y,
              batch_size=32,
              epochs=500,
              validation_split=0.2,
              callbacks=[tf.keras.callbacks.EarlyStopping(patience=3),
                         tf.keras.callbacks.TensorBoard(tb_log_dir)
                         ],
              )

    model.save_weights(model_h5)

    # 相对误差
    error = model.predict(train_X) - train_Y
    with open(os.path.join(RESULT_DIR, 'results.txt'), 'a') as fp:
        fp.write(f"-------{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}----------\n")
        fp.write(f'name: {data_name}\n')
        fp.write(f'is_dq: {dq}\n')
        fp.write(f'MAE: {np.mean(np.abs(error), axis=0).round(4)} \n')
        fp.write(f'RMSE: {np.sqrt(np.mean(np.square(error), axis=0)).round(4)} \n')
        fp.write('-------------------------------------------')


if __name__ == '__main__':
    from glob import glob
    for filename in glob(os.path.join(DATA_DIR, 'SRM-11月24日', '*.csv')):
        print(filename)
        train_on_data(filename, dq=True)
