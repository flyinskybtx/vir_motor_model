
class MoveState:
    def __init__(self):
        self.pos = 0
        self.vel = 0
        self.acc = 0
        self.jerk = 0


class MotorType:
    DC_Motor = 0  # 直流有刷电机
    PMS_Motor = 1  # 永磁同步
    Step_Motor2 = 2  # 两相步进
    Step_Motor3 = 3  # 三相步进电机
    SRM_Motor = 4  # 开关磁阻电机,同步磁阻电机
    ASY_Motor = 5  # 三相异步电机
    Linear_Motor = 6  # 直线电机
    VoiceCoil_Motor = 7  # 音圈电机


class SwitchState:
    OFF = 0  # 关
    ON = 1  # 开

