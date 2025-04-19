import psutil
import sys

def check_cpu():
    print(f"CPU usage: {psutil.cpu_percent(interval=1)}%")
    print(f"Number of CPU cores: {psutil.cpu_count(logical=True)}")

def check_memory():
    memory = psutil.virtual_memory()
    print(f"Total memory: {memory.total / (1024 ** 3):.2f} GB")
    print(f"Available memory: {memory.available / (1024 ** 3):.2f} GB")
    print(f"Memory usage: {memory.percent}%")

def check_disk():
    disk = psutil.disk_usage('/')
    print(f"Total Disk Space: {disk.total / (1024 ** 3):.2f} GB")
    print(f"Used Disk Space: {disk.used / (1024 ** 3):.2f} GB")
    print(f"Free Disk Space: {disk.free / (1024 ** 3):.2f} GB")
    print(f"Disk Usage: {disk.percent}%")

def main():
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg in ('--cpu'):
            check_cpu()
            return
        elif arg in ('--memory'):
            check_memory()
            return
        elif arg in ('--disk'):  # Fixed indentation here
            check_disk()
            return
        else:
            print(f"[!] Unknown command: {arg}")
            print("Run with --cpu, --memory or --disk to use")
            return

if __name__ == "__main__":
    main()

