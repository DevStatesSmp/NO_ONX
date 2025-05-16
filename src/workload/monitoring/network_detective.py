import psutil
import socket
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import csv
import os
import sys
import logging

def is_admin():
    if os.name == 'nt':  # Windows
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    else:
        # On non-Windows, always return False (no admin check)
        return False

# Thiết lập logging file + console
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("nettool.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Hỗ trợ xử lý Windows console encoding (nếu cần)
if os.name == 'nt':
    import ctypes
    ctypes.windll.kernel32.SetConsoleCP(65001)
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)

def ask_continue_on_interrupt():
    while True:
        ans = input("\nKeyboard Interrupt detected. Do you want to continue? (Y/n): ").strip().lower()
        if ans in ('y', ''):
            return True
        elif ans == 'n':
            print("Exiting... Goodbye!")
            return False
        else:
            print("Please enter Y or n.")

def net_traffic_monitor(interval=2, duration=30):
    """Giám sát lưu lượng mạng từng interface, tính max và mean"""
    logging.info(f"Start monitoring network traffic for {duration}s, interval {interval}s.")
    prev = {}
    stats = {}
    interfaces = psutil.net_io_counters(pernic=True)
    for i in interfaces:
        prev[i] = (interfaces[i].bytes_sent, interfaces[i].bytes_recv)
        stats[i] = {'max_up': 0, 'max_down': 0, 'sum_up': 0, 'sum_down': 0, 'count': 0}

    iterations = duration // interval
    try:
        for _ in range(iterations):
            time.sleep(interval)
            interfaces_new = psutil.net_io_counters(pernic=True)
            print(f"\n{'Interface':<15} {'Upload KB/s':>12} {'Download KB/s':>14}")
            print("-" * 43)
            for i, data in interfaces_new.items():
                sent = (data.bytes_sent - prev[i][0]) / 1024 / interval
                recv = (data.bytes_recv - prev[i][1]) / 1024 / interval
                prev[i] = (data.bytes_sent, data.bytes_recv)

                # Update stats
                stats[i]['sum_up'] += sent
                stats[i]['sum_down'] += recv
                stats[i]['count'] += 1
                if sent > stats[i]['max_up']:
                    stats[i]['max_up'] = sent
                if recv > stats[i]['max_down']:
                    stats[i]['max_down'] = recv

                print(f"{i:<15} {sent:12.2f} {recv:14.2f}")
    except KeyboardInterrupt:
        if not ask_continue_on_interrupt():
            return

    print("\n--- Statistics ---")
    for i in stats:
        count = stats[i]['count']
        mean_up = stats[i]['sum_up'] / count if count else 0
        mean_down = stats[i]['sum_down'] / count if count else 0
        print(f"{i:<15} Max Up: {stats[i]['max_up']:.2f} KB/s, Max Down: {stats[i]['max_down']:.2f} KB/s, Mean Up: {mean_up:.2f} KB/s, Mean Down: {mean_down:.2f} KB/s")
    logging.info("Network traffic monitoring finished.")

def conn_track(filter_status=None, max_show=20):
    """Xem danh sách kết nối với filter trạng thái và tên tiến trình"""
    logging.info(f"Listing active connections with filter_status={filter_status}")
    conns = psutil.net_connections()
    count = 0
    print(f"\n{'Local Address':<22} {'Remote Address':<22} {'Status':<13} {'PID':<6} {'Process Name'}")
    print("-" * 80)
    try:
        for c in conns:
            if filter_status and c.status != filter_status:
                continue
            try:
                pname = psutil.Process(c.pid).name() if c.pid else "N/A"
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pname = "N/A"
            laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else ""
            raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else ""
            print(f"{laddr:<22} {raddr:<22} {c.status:<13} {str(c.pid) if c.pid else 'N/A':<6} {pname}")
            count += 1
            if count >= max_show:
                break
    except KeyboardInterrupt:
        if not ask_continue_on_interrupt():
            return
    print()
    logging.info(f"Displayed {count} connections.")

def scan_port_worker(host, port, timeout):
    """Worker quét 1 port, trả về (port, banner) hoặc None"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((host, port))
            # Cố gắng nhận banner đơn giản
            s.settimeout(0.5)
            try:
                banner = s.recv(1024).decode(errors='ignore').strip()
            except:
                banner = ""
            return (port, banner)
        except:
            return None

def port_scan(host='127.0.0.1', start_port=1, end_port=1024, timeout=0.3, max_workers=100, save_file=None):
    """Quét port với ThreadPoolExecutor và lưu kết quả"""
    logging.info(f"Start port scanning {host}:{start_port}-{end_port} with timeout {timeout}s and max_workers {max_workers}")
    open_ports = []

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(scan_port_worker, host, port, timeout): port for port in range(start_port, end_port + 1)}
            for future in as_completed(futures):
                res = future.result()
                if res:
                    open_ports.append(res)
    except KeyboardInterrupt:
        if not ask_continue_on_interrupt():
            return

    if open_ports:
        print(f"Found {len(open_ports)} open ports on {host}:")
        for port, banner in sorted(open_ports):
            info = f" - Banner: {banner}" if banner else ""
            print(f"Port {port}{info}")
            if port not in (22, 80, 443):  # Ví dụ cảnh báo port không phổ biến
                logging.warning(f"Unusual open port detected: {port} on {host}")
    else:
        print("No open ports found.")
    logging.info("Port scanning finished.")

    if save_file:
        try:
            with open(save_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Host', 'Port', 'Banner'])
                for port, banner in open_ports:
                    writer.writerow([host, port, banner])
            logging.info(f"Port scan results saved to {save_file}")
        except Exception as e:
            logging.error(f"Failed to save scan results: {e}")
    print()

def networker_detective():
    while True:
        try:
            print("\n=== Network Tool for Windows (Enhanced) ===")
            print("1. Monitor Network Traffic")
            print("2. List Active Connections")
            print("3. Port Scan")
            print("4. Exit")
            choice = input("Choose an option: ").strip()
            if choice == '1':
                try:
                    interval = int(input("Enter interval (seconds, default 2): ") or 2)
                    duration = int(input("Enter duration (seconds, default 30): ") or 30)
                    net_traffic_monitor(interval=interval, duration=duration)
                except Exception as e:
                    logging.error(f"Error in Network Traffic Monitor: {e}")
            elif choice == '2':
                status = input("Filter by connection status (e.g., ESTABLISHED, LISTENING) or Enter for all: ").strip().upper()
                if not status:
                    status = None
                try:
                    max_show = int(input("Max connections to show (default 20): ") or 20)
                    conn_track(filter_status=status, max_show=max_show)
                except Exception as e:
                    logging.error(f"Error in Connection Tracker: {e}")
            elif choice == '3':
                host = input("Target host (default 127.0.0.1): ").strip() or "127.0.0.1"
                start_port = int(input("Start port (default 1): ") or 1)
                end_port = int(input("End port (default 1024): ") or 1024)
                timeout = float(input("Timeout per port in seconds (default 0.3): ") or 0.3)
                max_workers = int(input("Max threads (default 100): ") or 100)
                save_file = input("Save results to CSV file? Enter filename or leave empty: ").strip() or None
                try:
                    port_scan(host, start_port, end_port, timeout, max_workers, save_file)
                except Exception as e:
                    logging.error(f"Error in Port Scanner: {e}")
            elif choice == '4':
                print("Exiting program...")
                break
            else:
                print("Invalid choice. Please enter 1-4.")
        except KeyboardInterrupt:
            if not ask_continue_on_interrupt():
                break