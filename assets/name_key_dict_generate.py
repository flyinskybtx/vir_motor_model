
def generate_code(dict_name, name_key_dict):
    path = dict_name + '.py'
    f = open(path, 'w+')
    dict_head = dict_name + ' = {'
    n = len(dict_head)
    et = ''
    for j in range(n):
        et += ' '
    f.write(dict_head)
    first = 1
    for name in name_key_dict.keys():
        key = name_key_dict[name]
        if first == 1:
            s = "'" + name + "'" + ': ' + str(key) + ',\n'
            first = 0
        else:
            s = et + "'" + name + "'" + ': ' + str(key) + ',\n'
        f.write(s)
    f.write(et + '}\n')
    f.close()