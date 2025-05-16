import os
import platform
import psutil
import time
import wmi


def get_gpu_info():
    try:
        w = wmi.WMI()
        gpus = w.Win32_VideoController()
        gpu_info = []
        for gpu in gpus:
            gpu_info.append(f"{gpu.Name} ({'Integrated' if 'Intel' in gpu.Name else 'Physical'})")
        return ", ".join(gpu_info) if gpu_info else "Unknown"
    except Exception:
        return "Unknown"


def get_disk_info():
    try:
        partitions = psutil.disk_partitions()
        disk_info = []
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append(f"{partition.device} ({usage.total / (1024**3):.2f} GB)")
        return ", ".join(disk_info)
    except Exception:
        return "Unknown"


def get_system_info():
    print("\n\033[1m\033[92m[🔍 SYSTEM INFORMATION]\033[0m\n")
    print(f"\033[96m OS:\033[0m {platform.system()} {platform.release()} {platform.version()}")
    print(f"\033[96m Architecture:\033[0m {platform.architecture()[0]}")
    print(f"\033[96m CPU:\033[0m {platform.processor()}")
    print(f"\033[96m Cores:\033[0m {psutil.cpu_count(logical=True)} logical / {psutil.cpu_count(logical=False)} physical")
    print(f"\033[96m RAM:\033[0m {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
    uptime = round((time.time() - psutil.boot_time()) / 3600, 2)
    print(f"\033[96m Uptime:\033[0m {uptime} hours")
    print(f"\033[96m Kernel:\033[0m {platform.release()}")
    print(f"\033[96m GPU(s):\033[0m {get_gpu_info()}")
    print(f"\033[96m Disks:\033[0m {get_disk_info()}\n")