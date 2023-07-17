import system_detection

def print_dict_as_columns(data_dict, indent=0):
    for key, value in data_dict.items():
        if isinstance(value, dict):
            print(' ' * indent + f"{key}:")
            print_dict_as_columns(value, indent + 4)
        else:
            print(' ' * indent + f"{key}: {value}")

def main():
    print("欢迎使用系统信息检测工具！")
    detected_system = system_detection.detect_system()

    if detected_system == "windows":
        import windows_sys
        print("检测到 Windows 系统")
        all_info = windows_sys.get_all_info()
    elif detected_system == "linux":
        import linux_sys
        print("检测到 Linux 系统")
        all_info = linux_sys.get_all_info()
    else:
        print("未能识别的系统类型")
        return

    # 输出全部信息
    for info_type, info in all_info.items():
        print(f"\n【{info_type}】")
        if isinstance(info, list):  # 判断是否为列表
            if info_type == "CPU Info":
                info_str = ', '.join(info)  # 将多个 CPU 信息合并为一个字符串
                print(info_str)
            else:
                for item in info:
                    print(item)  # 增加缩进，使输出格式一致
        elif isinstance(info, dict):  # 判断是否为字典
            for key, value in info.items():
                print(f'    {key}: {value}')  # 使用缩进打印字典的键和值
        else:
            print(info)

if __name__ == "__main__":
    main()
