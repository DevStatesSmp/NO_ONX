import pyfiglet
import subprocess
import shutil
import sys
import distro
import psutil
import platform
import os

term_width = shutil.get_terminal_size().columns

ascii_banner = pyfiglet.figlet_format("NO_ONX", font="slant")
banner_lines = ascii_banner.splitlines()

max_line_length = max(len(line) for line in banner_lines)

for line in banner_lines:
    print(line)

version_str = "v0.1.2 beta" 
space_to_right = max_line_length - len(version_str)
print(" " * space_to_right + version_str + "\n")
print("📖 Usage: python3 <module_name>.py or python3 noonx.py <command>\n")

### ==== Command info ====

def show_help():
    print("""
usage:
    1. python3 noonx.py <command>
    or
    2. python3 [FILE_MODULE_NAME].py

Available module:
    detective      - Monitor file & system changes
    readfile       - Read file content
    
Scanning module:
    network_scan    - Scan ports or network issues
    file_scan       - Scan files for threats
    malware_scan    - Malware signature scanner

Option:
    --help (-h)          - Show help
    --system_info (-si)  - Check system infomation
""")

### ==== System info ====
def get_gpu_info():
    try:
        with os.popen("lspci | grep VGA") as f:
            return f.read().strip()
    except Exception as e:
        return f"Could not retrieve GPU info: {e}"

def get_system_info():
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
    
    

def main():
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg in ('--help', '-h'):
            show_help()
            return
        elif arg in ('--system_info', '--si'):
            get_system_info()
            return
        else:
            print(f"[!] Unknown command: {arg}")
            print("Run with --help for available commands.")
            return
    
main()
print("Use --help for more commands")

