
# 零部件模块
# 弹簧、开关、编码器、电流采样adc，鼠标交互
# 如果未注明单位就是标准单位，如果注明单位，到内部需要考虑单位转化
# 所有数据都在数据字典中，这里只定义数据名，通过数据名对数据进行操作
import math

from dige_stl.basic_library.base_data_type import SwitchState
from dige_stl.virtual_model_library.data_dict import OD
from dige_stl.virtual_model_library.vir_device_enum_data import VirEncoderType

class VirEncoderParam:  # 数据库是全的 ，根据不同编码器类型配置对应参数
    def __init__(self, key, first_name, data_dict):
        self.encoder_type = OD(key, first_name + 'encoder_type', VirEncoderType.Enc_Non, 'float32', data_dict)  # 编码器类型
        key += 1
        self.dpi_um = OD(key, first_name + 'dpi_um', 1, 'float32', data_dict)  # 光栅分辨率
        key += 1
        self.pole_pitch_mm = OD(key, first_name + 'pole_pitch_mm', 32, 'float32', data_dict)  # 极距
        key += 1
        self.lines = OD(key, first_name + 'lines', 4096, 'float32', data_dict)  # 编码器线数，倍频后
        key += 1
        self.direction = OD(key, first_name + 'direction', 1, 'float32', data_dict)  # 方向1或则-1
        key += 1
        self.offset = OD(key, first_name + 'offset', 0, 'float32', data_dict)  # 单位是脉冲
        self.key_end = key


class VirEncoderData:
    def __init__(self, key, first_name, data_dict):
        self.enc_param = VirEncoderParam(key, first_name, data_dict)
        key = self.enc_param.key_end + 1
        self.enc_pos = OD(key, first_name + 'enc_pos', 0, 'float32', data_dict)
        self.key_end = key


class VirCurrentADCData:
    def __init__(self, key, first_name, data_dict):
        self.current_noise_amp = OD(key, first_name + 'current_noise_amp', 0.01, 'float32', data_dict)  # 电流噪声幅值
        key += 1
        self.Iu = OD(key, first_name + 'Iu', 0, 'float32', data_dict)
        key += 1
        self.Iv = OD(key, first_name + 'Iv', 0, 'float32', data_dict)
        key += 1
        self.Iw = OD(key, first_name + 'Iw', 0, 'float32', data_dict)
        self.key_end = key

class EnvironmentParam:  # 环境参数
    def __init__(self, key, first_name, data_dict):
        self.dt = OD(key, first_name + 'dt', 50.0e-6, 'float32', data_dict)
        key += 1
        self.g = OD(key, first_name + 'g', 9.8, 'float32', data_dict)  # 重力加速度
        key += 1
        self.tilt_angle = OD(key, first_name + 'tilt_angle', 0, 'float32', data_dict)  # 倾斜角度
        self.key_end = key

