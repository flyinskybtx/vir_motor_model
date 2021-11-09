import sys, os

work_dir = os.path.abspath( os.path.join(os.path.dirname(__file__), '../..') )
sys.path.append(work_dir)

import pandas as pd
import math
import matplotlib.pyplot as plt
from dige_stl.general_library.math_macro import CONST
from dige_stl.general_library.signal_generator import SignalParam, SignalType, SignalGenerator
from dige_stl.virtual_model_library.data_dict import DeviceDataModelDict
from dige_stl.virtual_model_library.vir_rotate_motor_data import VirRotateMotorData
from virtual_model.vir_sensor.virtual_current_ADC import VirMotorADCFactory
from virtual_model.vir_sensor.virtual_encoder import VirEncoderFactory
from virtual_model.vir_state_equation.load_equation import VirPMSLoadEquation
from virtual_model.vir_state_equation.motor_state_equation import MotorStateEquation



class VirRotaryMotorModel:
    def __init__(self):
        self.model_dict = DeviceDataModelDict()  # 模型对象字典
        key = 30
        name = 'rotary_'
        self.device_data = VirRotateMotorData(key, name, self.model_dict)
        self.state_equ = MotorStateEquation(self.device_data.motor, self.device_data.env_param.dt.value)
        self.motor_adc_factory = VirMotorADCFactory(self.device_data.motor.current_adc)
        self.current_adc = self.motor_adc_factory.create_motor(self.device_data.motor.param.motor_type.value)
        self.encoder_factory = VirEncoderFactory(self.device_data.motor.encoder)
        self.encoder = self.encoder_factory.create_encoder()
        self.pms_load_equ = VirPMSLoadEquation(self.device_data)
        self.state_equ.set_load_equ(self.pms_load_equ)  # 由于负载方程比较复杂，由外部传入
        self.sd2cnt = 0

    def flush(self):
        param = self.device_data.motor.param
        self.state_equ.flush(param.mass.value, param.friction.value, param.damp.value)
        lines = self.device_data.motor.encoder.enc_param.lines.value
        self.sd2cnt = lines*CONST.INV_TWO_PI
        self.current_adc.flush()
        self.encoder.flush()

    def running(self):
        self.state_equ.running()
        pos_cnt = self.state_equ.state.pos * self.sd2cnt
        self.encoder.running(pos_cnt)
        Ia, Ib = self.state_equ.get_Iab()
        self.current_adc.running(Ia, Ib)
        self.output_data()

    def output_data(self):
        output = self.device_data.motor.output
        output.Ia.value = self.state_equ.ele_equ.Ia
        output.Ib.value = self.state_equ.ele_equ.Ib
        output.Id.value = self.state_equ.state.Id
        output.Iq.value = self.state_equ.state.Iq
        output.pos.value = self.state_equ.state.pos_abs
        output.vel.value = self.state_equ.state.vel
        output.acc.value = self.state_equ.state.acc


if __name__ == '__main__':
    class DeviceTest:
        def __init__(self):
            self.test_motor = VirRotaryMotorModel()
            self.test_motor.flush()
            self.dt = self.test_motor.device_data.env_param.dt.value
            self.sde_param = SignalParam()
            self.sde_param.amp = 10
            self.sde_param.fre_hz = 5
            self.sde_param.signal_type = SignalType.Signal_Type_Triangle
            self.sde_signal = SignalGenerator()
            self.sde_signal.set_param(self.sde_param, self.dt)
            self.uab_amp = 2
            self.num = int(1e5)
            self.sd_list = []
            self.ua_list = []
            self.Ia_list = []
            self.pos_list = []
            self.vel_list = []
            self.acc_list = []

        def uab_test_run(self):
            sde = self.sde_signal.get_signal()
            ua = self.uab_amp * math.cos(sde)
            ub = self.uab_amp * math.sin(sde)
            self.ua_list.append(ua)
            self.sd_list.append(sde)
            motor_input = self.test_motor.device_data.motor.input
            motor_input.Ua.value = ua
            motor_input.Ub.value = ub
            motor_input.enable.value = 1
            self.test_motor.running()
            output = self.test_motor.device_data.motor.output
            self.Ia_list.append(output.Ia.value)
            self.pos_list.append(output.pos.value)
            self.vel_list.append(output.vel.value)
            self.acc_list.append(output.acc.value)

        def test_run(self):
            for i in range(self.num):
                self.uab_test_run()

    device_test = DeviceTest()
    device_test.test_run()

    ax = plt.subplot(231)
    plt.plot(device_test.ua_list)
    ax.set_title('ua', fontsize=12)
    ax = plt.subplot(232)
    plt.plot(device_test.Ia_list)
    ax.set_title('ia', fontsize=12)
    ax = plt.subplot(233)
    plt.plot(device_test.sd_list)
    ax.set_title('sd', fontsize=12)
    # plt.show()
    ax = plt.subplot(234)
    plt.plot(device_test.pos_list)
    ax.set_title('pos', fontsize=12)
    ax = plt.subplot(235)
    plt.plot(device_test.vel_list)
    ax.set_title('vel', fontsize=12)
    ax = plt.subplot(236)
    plt.plot(device_test.acc_list)
    ax.set_title('acc', fontsize=12)
    plt.tight_layout()
    plt.show()
