import pyfiglet
import platform
import psutil
import distro
import os
import subprocess
import shutil

term_width = shutil.get_terminal_size().columns

ascii_banner = pyfiglet.figlet_format("NO_ONX", font="slant")
banner_lines = ascii_banner.splitlines()

max_line_length = max(len(line) for line in banner_lines)

for line in banner_lines:
    print(line)

version_str = "v0.1.2 beta" 
space_to_right = max_line_length - len(version_str)
print(" " * space_to_right + version_str + "\n")


def get_gpu_info():
    try:
        with os.popen("lspci | grep VGA") as f:
            return f.read().strip()
    except Exception as e:
        return f"Could not retrieve GPU info: {e}"

# System Information Output
def get_system_info():
    print("📌 NO_ONX - Analytical, investigattion, security monitoring for Linux System\n")
    
    # System
    print("\033[1mYour hardware system\033[0m\n")
    print(f"🖥️  OS: {distro.name(pretty=True)}")
    print(f"🧠  RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
    print(f"🔢 CPU: {platform.processor() or 'Unknown'}")
    print(f"⚙️  Cores: {psutil.cpu_count(logical=True)} (logical) | {psutil.cpu_count(logical=False)} (physical)")
    print(f"🕒 Uptime: {round((psutil.boot_time() - psutil.boot_time() % 60) / 60)} minutes since last boot")
    print(f"🧾 Kernel: {platform.release()}")
    print(f"🖼️  GPU: {get_gpu_info()}")
    print(f"🔍 Distro ID: {distro.id()}, Version: {distro.version()}\n")
    
get_system_info()
print("use python help.py to look out some commands")
