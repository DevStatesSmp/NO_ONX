import os
import platform
import psutil
import time

def get_gpu_info():
    try:
        gpu_info = os.popen("wmic path win32_VideoController get name").read().split("\n")
        gpu_names = [line.strip() for line in gpu_info if line.strip() and "Name" not in line]
        return ", ".join(gpu_names) if gpu_names else "Unknown"
    except Exception:
        return "Unknown"
    
def get_system_info():
    print("\n\033[1m\033[92m[🔍 SYSTEM INFORMATION]\033[0m\n")
    print(f"\033[96m OS:\033[0m {platform.system()} {platform.version()}")
    print(f"\033[96m RAM:\033[0m {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
    print(f"\033[96m CPU:\033[0m {platform.processor() or 'Unknown'}")
    print(f"\033[96m Cores:\033[0m {psutil.cpu_count(logical=True)} logical / {psutil.cpu_count(logical=False)} physical")
    uptime_min = round((time.time() - psutil.boot_time()) / 60)
    print(f"\033[96m Uptime:\033[0m {uptime_min} minutes")
    print(f"\033[96m Kernel:\033[0m {platform.release()}")
    print(f"\033[96m GPU:\033[0m {get_gpu_info()}")
    print(f"\033[96m Distro ID:\033[0m {platform.system()}, Version: {platform.version()}\n")