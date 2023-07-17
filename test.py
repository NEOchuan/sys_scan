import psutil
import wmi


network_info = []
wmi_obj = wmi.WMI()
for interface in wmi_obj.Win32_NetworkAdapterConfiguration(IPEnabled=True):
    ip_addresses = []
    for addr in psutil.net_if_addrs().get(interface.Description, []):
        if addr.family == psutil.AF_INET:
            ip_addresses.append(addr.address)

    subnet_mask = None
    for addr in psutil.net_if_addrs().get(interface.Description, []):
        if addr.family == psutil.AF_INET and addr.netmask:
            subnet_mask = addr.netmask

    if not ip_addresses:  # 如果IP地址为空，不加入列表
        continue

    ip_addresses_str = ', '.join(ip_addresses)
    subnet_mask_str = str(subnet_mask)

    info = {
        'name': interface.Description,
        'mac_address': interface.MACAddress,
        'ip_addresses': ip_addresses_str,
        'subnet_mask': subnet_mask_str,
    }
    network_info.append(info)
    print(info)
    print(network_info)

