# 有多种电机，有多种电机电气方程
from dige_stl.basic_library.base_data_type import MotorType
from dige_stl.general_library.math_lib import limit_cycle, anti_clockwise_conv, clockwise_conv
from dige_stl.general_library.math_macro import CONST
from dige_stl.virtual_model_library.vir_motor_data import VirMotorData
from virtual_model.vir_state_equation.virtual_device_state import VirState


class MotorElectricEquation:  # 通过修饰变成各类电机
    def __init__(self, motor_data: VirMotorData):
        self.motor_data = motor_data
        self.motor_param = self.motor_data.param

        self.R0 = 0.5
        self.TCR = 0
        self.Lq = 1.0e-3
        self.Lq_inv = 0
        self.KF = 0.07
        self.B = 0
        self.Fe = 0
        self.R = 0
        self.dIq = 0
        self.Ia = 0
        self.Ib = 0
        self.set_temperature(0)

    def set_temperature(self, temp):
        self.R = self.R0 * (1 + self.TCR * temp)

    def flush(self):
        self.R0 = self.motor_param.R0.value
        self.Lq = self.motor_param.Lq.value
        self.Lq_inv = 1 / self.Lq
        self.KF = self.motor_param.kF.value
        self.B = self.KF / 1.5  # 音圈电机默认极距为2pi m

    def running(self, X: VirState): pass


class PMSMotorElectricEquation(MotorElectricEquation):  # 通过修饰变成各类电机
    def __init__(self, motor_data: VirMotorData):
        super().__init__(motor_data)
        self.Ld = 1.0e-3
        self.Ld_inv = 0
        self.dId = 0
        self.Pn = 1
        self.flush()

    def flush(self):
        self.R0 = self.motor_param.R0.value
        self.Lq = self.motor_param.Lq.value
        self.Ld = self.motor_param.Ld.value
        self.Lq_inv = 1 / self.Lq
        self.Ld_inv = 1 / self.Ld
        self.KF = self.motor_param.kF.value
        self.Pn = self.motor_data.param.Pn.value
        self.B = self.KF / self.Pn / 1.5

    def running(self, X: VirState):
        angle_e = X.pos * self.Pn
        angle_e = limit_cycle(angle_e, CONST.TWO_PI)  # 限制在0~2pi之间
        Ud, Uq = anti_clockwise_conv(angle_e, self.motor_data.input.Ua.value, self.motor_data.input.Ub.value)
        # 电气方程
        angle_vel = X.vel * self.Pn
        BEMF_d = self.R * X.Id - self.Lq * X.Iq * angle_vel
        BEMF_q = self.R * X.Iq + (self.Ld * X.Id + self.B) * angle_vel
        if self.motor_data.input.enable.value == 1:
            self.dId = (Ud - BEMF_d) * self.Ld_inv
            self.dIq = (Uq - BEMF_q) * self.Lq_inv
            self.Fe = 1.5 * self.Pn * X.Iq * (self.B + (self.Ld - self.Lq) * X.Id)  # 电磁力

        else:  # 使能后电气方程失效
            self.dId = 0
            self.dIq = 0
            self.Fe = 0
            X.Id = 0
            X.Iq = 0
        self.Ia, self.Ib = clockwise_conv(angle_e, X.Id, X.Iq)


class ElectricEquationFactory:
    def __init__(self, motor_data: VirMotorData):
        self.motor_data = motor_data
        self.pms_motor_ele = PMSMotorElectricEquation(self.motor_data)

    def create_electric_equation(self):
        if self.motor_data.param.motor_type.value == MotorType.PMS_Motor:
            return self.pms_motor_ele
