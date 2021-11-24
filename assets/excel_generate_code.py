
# 将excel 自动生成python代码，缩短加载时间
import xlrd


class ExcelGenerateCode:
    def __init__(self):
        self.path = 'data_model.xlsx'
        self.name_list = ['rotary_motor_model', 'pipe_motor_model', 'linear_motor_model',
                          'force_control_model', 'slide_table_model', 'voice_coil_motor_model']  # 数据表名单
        self.data_list = []
        self.excel_file = xlrd.open_workbook(self.path)
        self.read_dict()
        self.generate_code()

    def read_dict(self):
        for model_name in self.name_list:
            table = self.excel_file.sheet_by_name(model_name)
            table._cell_values.pop(0)
            table_list = []
            for row_data in table._cell_values:
                table_list.append(row_data)
            self.data_list.append(table_list)

    def generate_code(self):
        path = 'data_dict_load.py'
        f = open(path, 'w+')
        data_len = len(self.name_list)
        for i in range(data_len):
            dict_head = self.name_list[i] + '_dict = {'
            n = len(dict_head)
            et = ''
            for j in range(n):
                et += ' '
            f.write(dict_head)
            first = 1
            for data in self.data_list[i]:
                key = str(int(data[0]))
                value = str(data[1:])
                if first == 1:
                    s = key + ': ' + value + ',\n'
                    first = 0
                else:
                    s = et + key + ': ' + value + ',\n'
                # s.encode('utf-8')
                f.write(s)
            f.write(et + '}\n')
        # 生成总表
        dict_head = 'data_model_dict_load = {'
        n = len(dict_head)
        et = ''
        for j in range(n):
            et += ' '
        f.write(dict_head)
        first = 1
        for name in self.name_list:
            key = "'" + name + '_dict' + "'"
            value = name + '_dict'
            if first == 1:
                s = key + ': ' + value + ',\n'
                first = 0
            else:
                s = et + key + ': ' + value + ',\n'
            # s.encode('utf-8')
            f.write(s)
        f.write(et + '}\n')
        f.close()


if __name__ == "__main__":
    test = ExcelGenerateCode()
    print(test.path)

