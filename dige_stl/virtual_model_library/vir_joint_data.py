from dige_stl.virtual_model_library.data_dict import OD
from dige_stl.virtual_model_library.vir_device_enum_data import VirDeviceType
from dige_stl.virtual_model_library.vir_motor_data import VirMotorData
from dige_stl.virtual_model_library.vir_parts_data import MouseData, EnvironmentParam, VirEncoderData, \
    VirTorqueSensorData


class VirJointParam:
    def __init__(self, key, first_name, data_dict):
        self.reduction_ratio = OD(key, first_name + 'damp', 50, 'float32', data_dict)
        key += 1
        self.damp = OD(key, first_name + 'damp', 0, 'float32', data_dict)
        key += 1
        self.fric = OD(key, first_name + 'damp', 0, 'float32', data_dict)
        key += 1
        self.arm_length = OD(key, first_name + 'arm_length', 0, 'float32', data_dict)
        key += 1
        self.arm_angle = OD(key, first_name + 'arm_angle', 0, 'float32', data_dict)
        key += 1
        self.load_mass = OD(key, first_name + 'load_mass', 0, 'float32', data_dict)
        self.key_end = key


class VirJointData:  # 后续还需增加属性，限位，力传感器
    def __init__(self, key, first_name, model_dict):
        name = first_name + 'device_type'
        self.device_type = OD(key, name, VirDeviceType.vir_joint, 'int32', model_dict)
        name = first_name + 'motor_'
        self.motor = VirMotorData(key, name, model_dict)
        key = self.motor.key_end + 1
        name = first_name + 'evn_'
        self.env_param = EnvironmentParam(key, name, model_dict)  # 可以设置竖直方向的直线电机
        name = first_name + 'mouse_'
        self.mouse = MouseData(key, name, model_dict)
        key = self.mouse.key_end + 1
        name = first_name + 'enc_'
        self.joint_encoder = VirEncoderData(key, first_name, model_dict)  # 关节输出编码器，有些有，有些没有
        key = self.joint_encoder.key_end + 1
        name = first_name + 'torque_sensor_'
        self.torque_sensor = VirTorqueSensorData(key, first_name, model_dict)  # 有些有力传感器，有些没有
        key = self.torque_sensor.key_end + 1
        name = first_name + 'param_'
        self.joint_param = VirJointParam(key, first_name, model_dict)
        self.key_end = self.joint_param.key_end

