import math

import numpy as np


def limit_range(x, x_min, x_max):
    y = x
    if x < x_min:
        y = x_min
    elif x > x_max:
        y = x_max
    return y


def limit_cycle(x, T):
    x_cyc = np.fix(x / T)  # 注意取证方式
    if x < 0:
        x_cyc -= 1
    x_lim = x - x_cyc * T
    return x_lim


def my_sin_cos(x):
    sin_x = np.sin(x)
    cos_x = np.cos(x)
    return sin_x, cos_x


def anti_clockwise_conv(sd, xa, xb):
    """ Park Transform"""
    sin_sd = math.sin(sd)
    cos_sd = math.cos(sd)
    xd = xa*cos_sd + xb*sin_sd
    xq = -xa*sin_sd + xb*cos_sd
    return xd, xq


def clockwise_conv(sd, xd, xq):
    """ Inverse Park Transform"""
    sin_sd = math.sin(sd)
    cos_sd = math.cos(sd)
    xa = xd*cos_sd + xq*sin_sd
    xb = -xd*sin_sd + xq*cos_sd
    return xa, xb

