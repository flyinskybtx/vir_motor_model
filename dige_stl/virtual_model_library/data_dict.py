class OD:  # 随着开发的需要不断完善
    def __init__(self, key, name, value, data_type, data_dict):
        self.key = key
        self.name = name
        self.unit = 'one'
        self.value = value
        self.type = data_type  # 类型
        data_dict.key_value_dict[key] = self

    def set_value(self, data):  # 有些需要调用通信协议将数据发出
        self.value = data

    def get_value(self):  # 发送获取数据的协议
        return self.value


class DeviceDataModelDict:
    def __init__(self):
        self.key_value_dict = dict()  # 所有模块都通过数据字典进行交互
        self.name_key_dict = dict()  # 手动写，可以自动生成

    def generate_name_key_dict(self):
        for key in self.key_value_dict.keys():
            self.name_key_dict[self.key_value_dict[key].name] = key

    def set_key_value(self, key, value):
        if key in self.key_value_dict.keys():
            self.key_value_dict[key].set_value(value)

    def get_key_value(self, key):
        if key in self.key_value_dict.keys():
            return self.key_value_dict[key].get_value()
        return None

    def set_name_value(self, name, value):  # 可以通过名字发送数据，也可以通过key发送数据
        if name in self.name_key_dict.keys():
            key = self.name_key_dict[name]
            if key in self.key_value_dict.keys():
                self.key_value_dict[key].set_value(value)

    def get_name_value(self, name):
        if name in self.name_key_dict.keys():
            key = self.name_key_dict[name]
            if key in self.key_value_dict.keys():
                data = self.key_value_dict[key].value
                return data
        return None

    def get_name_unit(self, name):
        if name in self.name_key_dict.keys():
            key = self.name_key_dict[name]
            if key in self.key_value_dict.keys():
                unit = self.key_value_dict[key].unit
                return unit
            print('no unit')
        print('no one')
        return None

# class DataDict:  # 通过excel自动生成
#     def __init__(self):
#         self.data_dict = dict()
#         self.read_dict()
#
#     def read_dict(self):
#         for name in data_model_dict_load.keys():
#             data_model_dict = DeviceDataModelDict()
#             key_value_dict = dict()
#             name_key_dict = dict()
#             model_data = data_model_dict_load[name]
#             for key in model_data.keys():
#                 data_od = OD()
#                 data_od.key = key
#                 data_od.name = model_data[key][0]
#                 data_od.unit = model_data[key][1]
#                 data_od.value = model_data[key][2]
#                 data_od.type = model_data[key][3]
#                 key_value_dict[key] = data_od
#                 name_key_dict[data_od.name] = data_od.key
#                 data_model_dict.key_value_dict = key_value_dict
#                 data_model_dict.name_key_dict = name_key_dict
#             self.data_dict[name] = data_model_dict
#
#
# if __name__ == "__main__":
#     test_data_dict = DataDict()
#     print(test_data_dict)
