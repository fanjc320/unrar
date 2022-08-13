#from unrar import rarfile
import rarfile
import itertools as its
import time
import threading

g_history = ""

def get_pwd(file, output_path, pwd):
    # 尝试解压来判断密码是否正确
    global g_history
    try:
        file.extractall(path=output_path, pwd=pwd)  # 解压到同名文件夹下
        # 说明当前密码有效，并告知
        g_history += " " + pwd
        print('-->Find password is "{}"'.format(pwd))
        global right_pwd
        right_pwd = pwd  # 将密码传出
        return right_pwd
    except:  # Exception as e
        return False


def get_password(min_digits, max_digits, words):
    """
    密码生成器
    :param min_digits: 密码最小长度
    :param max_digits: 密码最大长度
    :param words: 密码可能涉及的字符
    :return: 密码生成器
    """
    while min_digits <= max_digits:
        pwds = its.product(words, repeat=min_digits)  # 生成密码
        for pwd in pwds:  # 按顺序取出密码
            yield ''.join(pwd)  # 取出一个密码就传出一个密码
        min_digits += 1  # 长度增加1位


def find():
    #file_path = str(input('请输入要破解的压缩包位置：'))
    file_path = 'D:\old\Doc.rar'
    file = rarfile.RarFile(file_path)
    output_path = file_path.replace('.rar', '\\')

    # 密码范围
    wordstype_all = ['0546827913',
                     'jfhgurmvytnbiekdcowlsxpqaz',
                     'JFHGURMVYTNVIEKDCOWLSXPQAZ',
                     '~!@#$%^&*()_+{|}:"<>?`-=[]\;\',./'
                     ]
    print('请指定密码可能涉及的字符:')
    print('1.数字')
    print('2.小写英文字母')
    print('3.大写英文字母')
    print('4.特殊字符')
    print('5.上述组合')
    wordstype = input('6.自定义\n')
    if wordstype == '1':
        words = '0546827913'
    elif wordstype == '2':
        words = 'jfhgurmvytnbiekdcowlsxpqaz'
    elif wordstype == '3':
        words = 'JFHGURMVYTNVIEKDCOWLSXPQAZ'
    elif wordstype == '4':
        words = '~!@#$%^&*()_+{|}:"<>?`-=[]\;\',./'
    elif wordstype == '5':
        comwords = input('请指定组合类型（如2,1或3,4）：')
        comlist = comwords.split(',')
        words = ''
        for i in comlist:
            words = words + wordstype_all[int(i) - 1]
    elif wordstype == '6':
        words = input('请输入可能涉及的字符：')
    #words = 'fanjcsai012358'
    #words = 'fanjcsaiFANJCSAI012358'
    min_digit = int(input('请指定密码最小长度:'))
    max_digit = int(input('请指定密码最大长度:'))
    all = 0
    for digit in range(min_digit, max_digit + 1):
        all = all + pow(len(words), digit)
    print('共有{:.0f}个密码待尝试'.format(all))
    print('预计耗时{:.1f}个小时'.format(all * 0.0000009))
    input('按任意键继续，或按ctrl+c退出')
    pwds = get_password(min_digit, max_digit, words)
    # 开始查找密码
    start = time.time()
    thr = 0
    for i in range(1, all + 1):
        dur = time.time() - start
        print("\r破解中，已尝试{:.1f}%，耗时{:.0f}s".format(i / all * 100, dur), end='')  # 进度条
        try:
            pwd = next(pwds)
            try:
                th = threading.Thread(target=get_pwd, args=(file, output_path, pwd))  # 多线程破解
                th.start()
            except:  # Exception as e
                pass
        except StopIteration:
            print('已遍历所有可能，程序结束')
            thr = 1
            break

    # 等待所有线程跑完
    if thr == 1:
        for th in threading.enumerate():
            if th is threading.current_thread():
                continue
            th.join()

    end = time.time()
    print('-->总耗时{:.0f}s'.format(end - start))


def main():
    # 分析耗时
    # profile = line_profiler.LineProfiler(find)  # 把函数传递到性能分析器
    # profile.enable()  # 开始分析
    # find()
    # profile.disable()  # 停止分析
    # profile.print_stats()  # 打印出性能分析结果

    find()
    # 密码输出到破解文件所在文件夹内
    with open('password.txt', 'w') as f:
        f.write(right_pwd)

    with open('g_history.txt', 'w') as f:
        f.write(g_history)


main()