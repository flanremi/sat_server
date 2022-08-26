pre_filename = 'test_o1s120.txt'
filename = 'sat-bit-o1s120.txt'
lines = ''  # 用于将存储行的变量提前声明为string格式，避免编译器自动声明时可能由于第一行的特殊情况造成的数据类型错误

with open(pre_filename, 'r') as file_to_read:  # 打开文件
    while True:
        lines = file_to_read.readline()  # 整行读取数据
        if not lines:
            break
        else:
            if lines[0] == 'r':
                with open(filename, mode='a', encoding='utf-8') as file_obj:
                    file_obj.write(lines)
