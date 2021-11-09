import copy


class VirState:
    def __init__(self):
        self.pos_abs = 0  # 绝对位置
        self.pos = 0  # 单圈位置
        self.vel = 0
        self.acc = 0
        self.Id = 0
        self.Iq = 0

    def init(self, X):
        self.pos = copy.deepcopy(X.pos)
        self.vel = copy.deepcopy(X.vel)
        self.acc = copy.deepcopy(X.acc)
        self.Id = copy.deepcopy(X.Id)
        self.Iq = copy.deepcopy(X.Iq)

    def addition(self, X):
        self.pos += X.pos
        self.vel += X.vel
        self.acc += X.acc
        self.Id += X.Id
        self.Iq += X.Iq

    def subtraction(self, X):
        self.pos -= X.pos
        self.vel -= X.vel
        self.acc -= X.acc
        self.Id -= X.Id
        self.Iq -= X.Iq

    def scalar_multiplication(self, k):
        self.pos *= k
        self.vel *= k
        self.acc *= k
        self.Id *= k
        self.Iq *= k


