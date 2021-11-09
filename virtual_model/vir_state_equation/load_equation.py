# 负载方程，由于不同的模型受到的约束力不同，把所有约束力放到负载中，要做到统一是有难度的。
# 不过不妨碍在最高层形式上统一,所有弹簧，鼠标，重力等等都
from dige_stl.general_library.math_macro import CONST
from dige_stl.virtual_model_library.data_dict import DeviceDataModelDict
from dige_stl.virtual_model_library.vir_rotate_motor_data import VirRotateMotorData


class LoadEquation:
    def __init__(self):
        self.a = 0

    def flush(self): pass

    def running(self, pos, vel): pass


class VirPMSLoadEquation(LoadEquation):
    def __init__(self, pms_data: VirRotateMotorData):
        super().__init__()

    def running(self, pos, vel):
        return 0

