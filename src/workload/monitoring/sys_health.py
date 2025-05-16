import psutil
import time
import datetime
import platform
import os

def format_bytes(size):
    # format bytes thành KB, MB, GB dễ đọc
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def get_uptime():
    # uptime tính bằng giây
    boot_time = psutil.boot_time()
    now = time.time()
    uptime_sec = int(now - boot_time)
    return str(datetime.timedelta(seconds=uptime_sec))

def sys_health(detailed=True):
    print("=== System Health Report ===")
    print(f"Timestamp: {datetime.datetime.now()}")
    print(f"Platform: {platform.system()} {platform.release()} ({platform.version()})")
    print(f"Hostname: {platform.node()}")
    print(f"Uptime: {get_uptime()}")

    # CPU
    print("\n--- CPU ---")
    print(f"Physical cores: {psutil.cpu_count(logical=False)}")
    print(f"Total cores (logical): {psutil.cpu_count(logical=True)}")
    cpu_freq = psutil.cpu_freq()
    if cpu_freq:
        print(f"Max Frequency: {cpu_freq.max:.2f} MHz")
        print(f"Min Frequency: {cpu_freq.min:.2f} MHz")
        print(f"Current Frequency: {cpu_freq.current:.2f} MHz")
    print(f"CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"  Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")
    try:
        load1, load5, load15 = os.getloadavg()
        print(f"Load Average (1m,5m,15m): {load1:.2f}, {load5:.2f}, {load15:.2f}")
    except AttributeError:
        print("Load average not supported on this platform.")

    # Memory
    print("\n--- Memory ---")
    vm = psutil.virtual_memory()
    print(f"Total: {format_bytes(vm.total)}")
    print(f"Available: {format_bytes(vm.available)}")
    print(f"Used: {format_bytes(vm.used)} ({vm.percent}%)")
    print(f"Free: {format_bytes(vm.free)}")
    print(f"Active: {format_bytes(getattr(vm, 'active', 0))}")
    print(f"Inactive: {format_bytes(getattr(vm, 'inactive', 0))}")
    print(f"Buffers: {format_bytes(getattr(vm, 'buffers', 0))}")
    print(f"Cached: {format_bytes(getattr(vm, 'cached', 0))}")

    swap = psutil.swap_memory()
    print(f"\nSwap Total: {format_bytes(swap.total)}")
    print(f"Swap Used: {format_bytes(swap.used)} ({swap.percent}%)")
    print(f"Swap Free: {format_bytes(swap.free)}")
    print(f"Swap Sin/ Sout: {swap.sin} / {swap.sout}")

    # Disk
    print("\n--- Disk Partitions and Usage ---")
    partitions = psutil.disk_partitions(all=False)
    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            print(f"Device: {p.device} Mountpoint: {p.mountpoint} FileSystem: {p.fstype}")
            print(f"  Total Size: {format_bytes(usage.total)} Used: {format_bytes(usage.used)} ({usage.percent}%) Free: {format_bytes(usage.free)}")
        except PermissionError:
            print(f"  Device: {p.device} Mountpoint: {p.mountpoint} Permission Denied")

    # Disk IO
    print("\nDisk IO Counters (since boot):")
    io_counters = psutil.disk_io_counters()
    if io_counters:
        print(f"  Read Count: {io_counters.read_count}")
        print(f"  Write Count: {io_counters.write_count}")
        print(f"  Read Bytes: {format_bytes(io_counters.read_bytes)}")
        print(f"  Write Bytes: {format_bytes(io_counters.write_bytes)}")
        print(f"  Read Time: {io_counters.read_time} ms")
        print(f"  Write Time: {io_counters.write_time} ms")

    # Temperatures
    print("\n--- Temperature Sensors ---")
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                print(f"Sensor: {name}")
                for entry in entries:
                    label = entry.label or "Unknown"
                    print(f"  {label}: {entry.current}°C (High: {entry.high}°C, Critical: {entry.critical}°C)")
        else:
            print("No temperature sensors found.")
    else:
        print("Temperature sensor not supported on this platform.")

    # Network
    print("\n--- Network Interfaces ---")
    net_if_addrs = psutil.net_if_addrs()
    net_if_stats = psutil.net_if_stats()
    for iface, addrs in net_if_addrs.items():
        print(f"Interface: {iface}")
        if iface in net_if_stats:
            stats = net_if_stats[iface]
            print(f"  Status: {'Up' if stats.isup else 'Down'}")
            print(f"  Speed: {stats.speed} Mbps")
            print(f"  Duplex: {stats.duplex}")
            print(f"  MTU: {stats.mtu}")
        for addr in addrs:
            print(f"  Address Family: {addr.family.name if hasattr(addr.family, 'name') else addr.family}")
            print(f"    Address: {addr.address}")
            if addr.netmask:
                print(f"    Netmask: {addr.netmask}")
            if addr.broadcast:
                print(f"    Broadcast: {addr.broadcast}")
            if addr.ptp:
                print(f"    PTP: {addr.ptp}")

    # Network IO
    print("\nNetwork IO counters (since boot):")
    net_io = psutil.net_io_counters()
    print(f"  Bytes Sent: {format_bytes(net_io.bytes_sent)}")
    print(f"  Bytes Received: {format_bytes(net_io.bytes_recv)}")
    print(f"  Packets Sent: {net_io.packets_sent}")
    print(f"  Packets Received: {net_io.packets_recv}")
    print(f"  Errors In: {net_io.errin}")
    print(f"  Errors Out: {net_io.errout}")
    print(f"  Drop In: {net_io.dropin}")
    print(f"  Drop Out: {net_io.dropout}")

    print("\n--- System Processes ---")
    total_procs = len(psutil.pids())
    running_procs = len([p for p in psutil.process_iter(['status']) if p.info['status'] == psutil.STATUS_RUNNING])
    print(f"Total processes: {total_procs}")
    print(f"Running processes: {running_procs}")
    print()

def proc_watch(top_n=5):
    print(f"=== Top {top_n} Processes by CPU Usage ===")
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procs.append((p.info['cpu_percent'], p.info['memory_percent'], p.info['name'], p.info['pid']))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    procs.sort(reverse=True, key=lambda x: x[0])  # sort by cpu_percent descending
    for cpu, mem, name, pid in procs[:top_n]:
        print(f"PID {pid} - {name}: CPU {cpu:.2f}% | Memory {mem:.2f}%")
    print()

def sys_health():
    while True:
        print("Choose command:")
        print("1. sys_health")
        print("2. proc_watch")
        print("0. Exit")
        cmd = input("Enter choice: ").strip()

        if cmd == '1':
            sys_health()
        elif cmd == '2':
            try:
                top_n = int(input("How many top processes to show? (default 5): ") or "5")
            except:
                top_n = 5
            proc_watch(top_n)
        elif cmd == '0':
            break
        else:
            print("Invalid command. Try again.\n")

if __name__ == "__main__":
    sys_health()
