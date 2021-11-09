from dige_stl.basic_library.base_data_type import MotorType
from dige_stl.general_library.math_macro import CONST
from dige_stl.general_library.signal_generator import SignalParam, SignalType, SignalGenerator
from dige_stl.virtual_model_library.vir_parts_data import VirCurrentADCData


class VirtualCurrentADC:
    def __init__(self, current_adc: VirCurrentADCData):
        self.current_adc = current_adc
        self.signal_param = SignalParam()
        self.signal_param.signal_type = SignalType.Signal_Type_RandNorm
        self.current_noise = SignalGenerator()

    def flush(self):
        self.signal_param.amp = self.current_adc.current_noise_amp.value
        self.current_noise.set_param(self.signal_param, 1)

    def running(self, Ia, Ib): pass


class VirDCMotorADC(VirtualCurrentADC):
    def __init__(self, current_adc: VirCurrentADCData):
        super().__init__(current_adc)

    def running(self, Ia, Ib):  # 直流有刷电机，只有Ib有效，输出只有Iv有效
        self.current_adc.Iu.value = 0
        self.current_adc.Iv.value = Ib
        self.current_adc.Iw.value = 0
        self.current_adc.Iu.value += self.current_noise.get_signal()
        self.current_adc.Iv.value += self.current_noise.get_signal()
        self.current_adc.Iw.value += self.current_noise.get_signal()
        return self.current_adc.Iu.value, self.current_adc.Iv.value, self.current_adc.Iw.value


class VirPMSMotorADC(VirtualCurrentADC):
    def __init__(self, current_adc: VirCurrentADCData):
        super().__init__(current_adc)

    def running(self, Ia, Ib):
        self.current_adc.Iu.value = Ia
        self.current_adc.Iv.value = -0.5 * Ia + CONST.SQRT3_OVER_2 * Ib
        self.current_adc.Iw.value = - (self.current_adc.Iu.value + self.current_adc.Iv.value)
        self.current_adc.Iu.value += self.current_noise.get_signal()
        self.current_adc.Iv.value += self.current_noise.get_signal()
        self.current_adc.Iw.value += self.current_noise.get_signal()
        return self.current_adc.Iu.value, self.current_adc.Iv.value, self.current_adc.Iw.value


class VirStepMotor2ADC(VirtualCurrentADC):
    def __init__(self, current_adc: VirCurrentADCData):
        super().__init__(current_adc)

    def running(self, Ia, Ib):
        self.current_adc.Iu.value = Ia
        self.current_adc.Iv.value = -(Ia-Ib)
        self.current_adc.Iw.value = Ib
        self.current_adc.Iu.value += self.current_noise.get_signal()
        self.current_adc.Iv.value += self.current_noise.get_signal()
        self.current_adc.Iw.value += self.current_noise.get_signal()
        return self.current_adc.Iu.value, self.current_adc.Iv.value, self.current_adc.Iw.value


class VirMotorADCFactory:
    def __init__(self, current_adc: VirCurrentADCData):
        self.current_adc = current_adc
        self.dc_motor_adc = VirDCMotorADC(self.current_adc)
        self.pms_motor_adc = VirPMSMotorADC(self.current_adc)
        self.step_motor2_adc = VirStepMotor2ADC(self.current_adc)

    def create_motor(self, motor_type: MotorType):
        if motor_type == MotorType.DC_Motor:
            return self.dc_motor_adc
        elif motor_type == MotorType.PMS_Motor:
            return self.pms_motor_adc
        elif motor_type == MotorType.Step_Motor2:
            return self.step_motor2_adc
        elif motor_type == MotorType.Step_Motor3:
            return self.pms_motor_adc
        elif motor_type == MotorType.SRM_Motor:
            return self.pms_motor_adc
        elif motor_type == MotorType.ASY_Motor:
            return self.pms_motor_adc
        elif motor_type == MotorType.Linear_Motor:
            return self.pms_motor_adc
        if motor_type == MotorType.VoiceCoil_Motor:
            return self.dc_motor_adc
