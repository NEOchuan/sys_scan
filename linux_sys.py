import os
import socket
import netifaces
import psutil
from datetime import datetime

def timestamp_to_local_time(timestamp):
    local_time = datetime.fromtimestamp(timestamp)
    local_time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')
    return local_time_str



def get_network_info():
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


def get_disk_info():
    disk_info = []
    partitions = psutil.disk_partitions(all=True)
    for partition in partitions:
        mountpoint = partition.mountpoint
        usage = psutil.disk_usage(mountpoint)
        info = {
            'Mount Point': mountpoint,
            'File System Type': partition.fstype,
            'Total Size (GB)': round(usage.total / (1024 ** 3), 2),
            'Used (GB)': round(usage.used / (1024 ** 3), 2),
            'Free (GB)': round(usage.free / (1024 ** 3), 2),
            'Usage (%)': usage.percent,
        }
        disk_info.append(info)
    return disk_info


def get_boot_time():
    """获取系统启动时间"""
    boot_time = psutil.boot_time()
    boot_time_str = timestamp_to_local_time(boot_time)
    return boot_time_str


def get_processes():
    """获取正在运行的进程列表"""
    processes = []
    for process in psutil.process_iter(['pid', 'name', 'username']):
        processes.append({
            'pid': process.info['pid'],
            'name': process.info['name'],
            'username': process.info['username']
        })
    return processes

# 定义一个函数用于获取全部信息
def get_all_info():

    all_info = {
        "disk_info": get_disk_info() ,
        "network_info": get_network_info(),
        "software_info": get_processes(),
        "local_boot_time": get_boot_time(),
    }

    return all_info
