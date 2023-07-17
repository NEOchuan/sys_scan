import platform
import wmi
import psutil
import socket

def get_system_version():
    wmi_obj = wmi.WMI()
    os_version = wmi_obj.Win32_OperatingSystem()[0].Caption
    return os_version

def get_cpu_info():
    cpu_count = psutil.cpu_count(logical=False) # 获取物理核心数
    xc_count = psutil.cpu_count() # 获取线程数
    cpu_percent = round(psutil.cpu_percent(1), 2) # 获取 CPU 使用率
    cpu_info = ("CPU核心:" + str(cpu_count) + "\n" + "CPU线程:" + str(xc_count) + "\n" + "CPU使用率:" + str(cpu_percent))
    return cpu_info


def get_user_info():
    wmi_obj = wmi.WMI()
    user_info = wmi_obj.Win32_ComputerSystem()[0].UserName
    return user_info

def get_installed_software():
    wmi_obj = wmi.WMI()
    installed_software = []

    for program in wmi_obj.Win32_Product():
        installed_software.append(program.Caption)

    return installed_software


def get_disk_info():
    disk_info = []
    wmi_obj = wmi.WMI()
    for drive in wmi_obj.Win32_LogicalDisk(DriveType=3):
        try:
            total_space = int(drive.Size) / (1024 ** 3)
            free_space = int(drive.FreeSpace) / (1024 ** 3)
            used_space = total_space - free_space
            total_space_str = "{:.2f}".format(total_space)
            used_space_str = "{:.2f}".format(used_space)
            info = f"{drive.DeviceID} ({drive.FileSystem}) - 总空间: {total_space_str} GB, 已使用: {used_space_str} GB"
            disk_info.append(info)
        except Exception as e:
            print(f"获取硬盘信息失败：{e}")

    disk_info.sort(key=lambda x: x.split()[0])  # 假设设备号在硬盘信息中是第一个部分，使用空格进行分割
    return disk_info


def get_memory_info():
    svmem = psutil.virtual_memory()
    total_memory = svmem.total / (1024 ** 3)
    used_memory = svmem.used / (1024 ** 3)
    return f"总内存: {total_memory:.2f} GB, 已使用: {used_memory:.2f} GB"

def get_gpu_info():
    try:
        import pycuda.driver as cuda
        from pycuda import autoinit
        device = cuda.Device(0)
        gpu_name = device.name()
        driver_version = cuda.get_driver_version()
        return f"显卡型号: {gpu_name}, 驱动版本: {driver_version}"
    except ImportError:
        return "无法获取显卡信息，请安装 pycuda 模块。"

def get_network_interfaces():
    net_info = {}
    addrs = psutil.net_if_addrs()
    for interface_name, interface_addrs in addrs.items():
        net_info[interface_name] = {}
        for addr in interface_addrs:
            if addr.family == psutil.AF_LINK:
                net_info[interface_name]['mac'] = addr.address
            elif addr.family == socket.AF_INET:
                net_info[interface_name]['ipv4'] = addr.address
                net_info[interface_name]['ipv4_netmask'] = addr.netmask
            elif addr.family == socket.AF_INET6:
                net_info[interface_name]['ipv6'] = addr.address
    return net_info



def get_all_info():

    all_info = {
        "disk_info": get_disk_info(),
        "network_info": get_network_interfaces(),
        "installed_software": get_installed_software(),
        "cpu_info": get_cpu_info() ,
        "System_Version_info": get_system_version(),
        "user_info": get_user_info(),
    }

    return all_info