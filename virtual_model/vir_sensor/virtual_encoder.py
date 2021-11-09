# 当改变编码器类型时，需要重新构建，为了避免重新构建，也可以同时构建好，根据不同类型选择返回某个类型
# 后续再做优化
import copy

from dige_stl.general_library.math_lib import limit_cycle
from dige_stl.virtual_model_library.vir_device_enum_data import VirEncoderType
from dige_stl.virtual_model_library.vir_parts_data import VirEncoderData


class VirtualEncoder:  # 所有编码器都可以转化为，旋转编码器，传入底层编码器的数据都已经转化为单圈脉冲位置
    def __init__(self, enc_data: VirEncoderData):
        self.enc_data = enc_data
        self.lines = 0  # 可能会变，可能是直线编码器
        self.direction = enc_data.enc_param.direction
        self.enc_pos = enc_data.enc_pos
        self.line_half = 0

    def init(self): pass  # 回到初始状态，增量编码器

    def flush(self): pass

    def running(self, pos): pass


class VirtualEncRotateInc(VirtualEncoder):
    def __init__(self, enc_data: VirEncoderData):
        super().__init__(enc_data)
        self.lines = self.enc_data.enc_param.lines
        self.start_flag = 0
        self.start_pos = 0
        self.init()

    def init(self):
        self.start_flag = 0

    def flush(self):
        self.line_half = int(self.lines.value / 2)

    def running(self, pos):  # 旋转增量编码器，输入位置为单圈绝对
        if self.start_flag == 0:
            self.start_pos = pos  # 以第一个位置起点，计算增量
            self.start_flag = 1
        pos_in = (pos - self.start_pos)*self.direction.value
        pos_out = limit_cycle(pos_in, self.lines.value)
        self.enc_pos.value = copy.deepcopy(pos_out)
        return pos_out


class VirtualEncRotateAbs(VirtualEncoder):
    def __init__(self, enc_data: VirEncoderData):
        super().__init__(enc_data)
        self.offset = self.enc_data.enc_param.offset  # 绝对值编码器偏移
        self.lines = self.enc_data.enc_param.lines

    def flush(self):
        self.line_half = int(self.lines.value / 2)

    def running(self, pos):  # 输入位置为单圈绝对
        pos_in = (pos - self.offset.value)*self.direction.value
        pos_out = limit_cycle(pos_in, self.lines.value)
        self.enc_data.enc_pos.value = pos_out
        return pos_out


class VirtualEncNan(VirtualEncoder):
    def __init__(self, enc_data: VirEncoderData):
        super().__init__(enc_data)

    def running(self, pos):  # 输入位置为单圈绝对
        self.enc_pos.value = 0
        return 0


class VirtualEncLinearInc(VirtualEncoder):
    def __init__(self, enc_data: VirEncoderData):
        super().__init__(enc_data)
        self.start_flag = 0
        self.start_pos = 0
        self.init()

    def init(self):
        self.start_flag = 0

    def flush(self):
        self.lines = int(1000*self.enc_data.enc_param.pole_pitch_mm.value/self.enc_data.enc_param.dpi_um.value)
        self.line_half = int(self.lines / 2)

    def running(self, pos):  # 旋转增量编码器，输入位置为单圈绝对
        if self.start_flag == 0:
            self.start_pos = pos  # 以第一个位置起点，计算增量
            self.start_flag = 1
        pos_in = (pos - self.start_pos) * self.direction.value
        pos_out = limit_cycle(pos_in, self.lines)
        self.enc_data.enc_pos.value = pos_out
        return pos_out


class VirtualEncLinearAbs(VirtualEncoder):
    def __init__(self, enc_data: VirEncoderData):
        super().__init__(enc_data)
        self.offset = self.enc_data.enc_param.offset  # 绝对值编码器偏移

    def flush(self):
        self.lines = int(1000*self.enc_data.enc_param.pole_pitch_mm.value/self.enc_data.enc_param.dpi_um.value)
        self.line_half = int(self.lines / 2)

    def running(self, pos):  # 输入位置为单圈绝对
        pos_in = (pos - self.offset) * self.direction.value
        pos_out = limit_cycle(pos_in, self.lines)
        self.enc_pos.value = copy.deepcopy(pos_out)
        return pos_out


class VirEncoderFactory:   # 编码器工厂
    def __init__(self, enc_data: VirEncoderData):
        self.enc_data = enc_data

    def create_encoder(self):
        if self.enc_data.enc_param.encoder_type.value == VirEncoderType.Enc_Rotate_Inc:
            return VirtualEncRotateInc(self.enc_data)
        elif self.enc_data.enc_param.encoder_type.value == VirEncoderType.Enc_Rotate_Abs:
            return VirtualEncRotateAbs(self.enc_data)
        elif self.enc_data.enc_param.encoder_type.value == VirEncoderType.Enc_Linear_Inc:
            return VirtualEncRotateInc(self.enc_data)
        elif self.enc_data.enc_param.encoder_type.value == VirEncoderType.Enc_Linear_Abs:
            return VirtualEncRotateAbs(self.enc_data)
        elif self.enc_data.enc_param.encoder_type.value == VirEncoderType.Enc_Non:
            return VirtualEncNan(self.enc_data)

