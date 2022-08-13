#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import rarfile
import itertools
from threading import Thread
# 用排列组合生成包含大写字母和数字的8位密码列表
pass_wd_list = ("".join(x) for x in itertools.product('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890', repeat=8))

success = 0    # 记录破解成功标志
num_flg = 0    # 记录破解次数
file_name = r'D:\old\Doc.rar'     # 要破解的文件
file_path = r'D:\old\Doc_rar'             # 破解后解压位置

def get_now_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def decryptRarZipFile():
    global success, num_flg
    while success == 0:
        num_flg += 1
        pass_wd = next(pass_wd_list)

        fp = rarfile.RarFile(file_name)
        try:
            print("{} 当前密码为：{} {}".format(get_now_time(), pass_wd, num_flg))
            fp.extractall(path=file_path , pwd=pass_wd.encode())
            print("success! password is : {}".format(pass_wd))
            fp.close()
            success = 1    # 破解成功后改变标志值
        except TypeError as e:
            pass
        except StopIteration as e:
            break

# 没用
#if __name__ == '__main__':
def unrar1():
    start_time = time.time()
    decryptRarZipFile()
    end_time = time.time()
    change_time = end_time - start_time
    print("破解耗时：{}s".format(change_time))