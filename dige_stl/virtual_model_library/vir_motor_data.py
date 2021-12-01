from dige_stl.basic_library.base_data_type import MotorType
from dige_stl.virtual_model_library.data_dict import OD, DeviceDataModelDict
from dige_stl.virtual_model_library.vir_parts_data import VirCurrentADCData, VirEncoderData


class VirMotorParam:
    def __init__(self, key, first_name, data_dict):
        self.motor_type = OD(key, first_name + 'pos_mm', MotorType.SRM_Motor, 'int32', data_dict)
        key += 1
        self.R0 = OD(key, first_name + 'R0', 0.084, 'float32', data_dict)
        key += 1
        self.TCR = OD(key, first_name + 'TCR', 0, 'float32', data_dict)
        key += 1
        self.Ld = OD(key, first_name + 'Ld', 0.00485, 'float32', data_dict)  # 单位H
        key += 1
        self.Lq = OD(key, first_name + 'Lq', 0.00097, 'float32', data_dict)  # 单位H
        key += 1
        self.kF = OD(key, first_name + 'kF', 0.07, 'float32', data_dict)   # 力常数
        key += 1
        self.mass = OD(key, first_name + 'mass', 62.18, 'float32', data_dict)  # 质量或惯量
        key += 1
        self.friction = OD(key, first_name + 'friction', 0, 'float32', data_dict)   # 静摩擦
        key += 1
        self.damp = OD(key, first_name + 'damp', 1.0e-3, 'float32', data_dict)   # 阻尼
        key += 1
        self.Pn = OD(key, first_name + 'Pn', 4, 'int32', data_dict)   # 极对数
        key += 1
        self.pole_pitch_mm = OD(key, first_name + 'pole_pitch_mm', 32, 'float32', data_dict)  # 极距,永磁同步直线电机具有这个参数，音圈电机没有
        self.length_mm = OD(key, first_name + 'length_mm', 1000, 'float32', data_dict)
        self.key_end = key


class VirMotorInputData:
    def __init__(self, key, first_name, data_dict):
        self.Ua = OD(key, first_name + 'Ua', 0, 'float32', data_dict)
        key += 1
        self.Ub = OD(key, first_name + 'Ub', 0, 'float32', data_dict)
        key += 1
        self.enable = OD(key, first_name + 'enable', 0, 'int32', data_dict)
        self.key_end = key


class VirMotorOutputData:
    def __init__(self, key, first_name, data_dict):
        self.Ia = OD(key, first_name + 'Ia', 0, 'float32', data_dict)
        key += 1
        self.Ib = OD(key, first_name + 'Ib', 0, 'float32', data_dict)
        key += 1
        self.Id = OD(key, first_name + 'Id', 0, 'float32', data_dict)
        key += 1
        self.Iq = OD(key, first_name + 'Iq', 0, 'float32', data_dict)
        key += 1
        self.pos = OD(key, first_name + 'pos', 0, 'float32', data_dict)
        key += 1
        self.vel = OD(key, first_name + 'vel', 0, 'float32', data_dict)
        key += 1
        self.acc = OD(key, first_name + 'acc', 0, 'float32', data_dict)
        key += 1
        self.key_end = key


class VirMotorData:  # 电机数据 电机参数，电机状态，编码器，电流adc
    def __init__(self, key, first_name, data_dict):
        name = first_name + 'param_'
        self.param = VirMotorParam(key, name, data_dict)
        key = self.param.key_end + 1
        name = first_name + 'input_'
        self.input = VirMotorInputData(key, name, data_dict)
        key = self.input.key_end + 1
        name = first_name + 'output_'
        self.output = VirMotorOutputData(key, name, data_dict)
        key = self.output.key_end + 1
        name = first_name + 'adc_'
        self.current_adc = VirCurrentADCData(key, first_name, data_dict)
        key = self.current_adc.key_end + 1
        name = first_name + 'enc_'
        self.encoder = VirEncoderData(key, first_name, data_dict)
        self.key_end = key


if __name__ == '__main__':
    test_data_dict = DeviceDataModelDict()
    test_first_name = 'pms_'
    test_key = 10
    test_vir_pms_motor_data = VirMotorData(test_key, test_first_name, test_data_dict)

    print(test_vir_pms_motor_data)
