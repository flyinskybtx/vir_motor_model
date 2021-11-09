from dige_stl.virtual_model_library.data_dict import OD
from dige_stl.virtual_model_library.vir_device_enum_data import VirDeviceType
from dige_stl.virtual_model_library.vir_motor_data import VirMotorData
from dige_stl.virtual_model_library.vir_parts_data import EnvironmentParam


class VirRotateMotorData:
    def __init__(self, key, first_name, model_dict):
        name = first_name + 'device_type'
        self.device_type = OD(key, name, VirDeviceType.vir_rotate_motor, 'int32', model_dict)
        name = first_name + 'motor_'
        self.motor = VirMotorData(key, name, model_dict)
        key = self.motor.key_end + 1
        name = first_name + 'evn_'
        self.env_param = EnvironmentParam(key, name, model_dict)  # 可以设置竖直方向的直线电机
        key = self.env_param.key_end
        self.init()

    def init(self):
        self.motor.param.mass.value = 1.0e-2

