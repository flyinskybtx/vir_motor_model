
# 把所有电机都等价为旋转电机，对于音圈电机进行默认等价
from dige_stl.general_library.math_macro import CONST
from dige_stl.virtual_model_library.vir_motor_data import VirMotorData
from virtual_model.vir_state_equation.dynamic_equation import DynamicEquation
from virtual_model.vir_state_equation.electric_equation import ElectricEquationFactory
from virtual_model.vir_state_equation.load_equation import LoadEquation
from virtual_model.vir_state_equation.virtual_device_state import VirState


class MotorStateEquation:
    def __init__(self, motor_data: VirMotorData, dt):
        self.dt = dt
        self.motor_data = motor_data
        ele_equ_fact = ElectricEquationFactory(motor_data)
        self.ele_equ = ele_equ_fact.create_electric_equation()
        self.dyn_equ = DynamicEquation()
        self.load_equ = LoadEquation()
        self.state = VirState()  # VirState()  # 状态参数，其中位置是单圈，音圈电机极距为2pi
        self.cycle_pos = 0

    def flush(self, load_mass, load_fric, load_damp):
        self.state = VirState()  # 状态参数，其中位置是单圈，音圈电机极距为2pi
        self.dyn_equ.flush(load_mass, load_fric, load_damp)
        self.ele_equ.flush()
        self.load_equ.flush()

    def set_load_equ(self, load_equ):
        self.load_equ = load_equ

    def get_Iab(self):
        return self.ele_equ.Ia, self.ele_equ.Ib

    def running(self):
        dX = self.state_integral(self.state, self.dt)
        next_vel = self.state.vel + dX.vel
        dir = next_vel*self.state.vel
        if dir < 0:  # 发生过零
            start_dvt = self.state.vel/dX.vel*self.dt
            dX1 = self.state_integral(self.state, start_dvt)
            self.state.addition(dX1)
            self.state.vel = 0
            end_dvt = self.dt - start_dvt
            dX2 = self.state_integral(self.state, end_dvt)
            self.state.acc = 0
            self.state.addition(dX2)
        else:
            self.state.acc = 0
            self.state.addition(dX)
        # 位置限定范围，根据旋转和直线有不同
        if self.state.pos > CONST.TWO_PI:
            self.state.pos -= CONST.TWO_PI
            self.cycle_pos += CONST.TWO_PI
        elif self.state.pos < 0:
            self.state.pos += CONST.TWO_PI
            self.cycle_pos -= CONST.TWO_PI
        self.state.pos_abs = self.cycle_pos + self.state.pos

    def state_equation(self, X: VirState, dt):
        self.ele_equ.running(X)
        abs_pos = self.cycle_pos + X.pos
        f_load = self.load_equ.running(abs_pos, X.vel)
        f = self.ele_equ.Fe + f_load
        acc = self.dyn_equ.running(X, f)
        dX = VirState()
        dX.Id = self.ele_equ.dId*dt
        dX.Iq = self.ele_equ.dIq*dt
        dX.acc = acc
        dX.vel = acc*dt
        dX.pos = X.vel*dt
        return dX

    def two_order_integral(self, X: VirState, dt):
        self.dyn_equ.set_friction_direction(X.vel)
        dX = self.state_equation(X, dt)
        X2 = VirState()
        X2.init(X)
        X2.addition(dX)
        dX2 = self.state_equation(X2, dt)
        dX2.addition(dX)
        dX2.scalar_multiplication(0.5)
        return dX2

    def state_integral(self, X: VirState, dt):  # 后期有多中积分方法可选
        return self.two_order_integral(X, dt)
