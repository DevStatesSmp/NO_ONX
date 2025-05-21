import sys
import subprocess
import re
from datetime import datetime
from colorama import Fore, Style, init
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from src.utils.getError import handle_error, ErrorContent, ErrorReason

try:
    import win32evtlog
    import win32evtlogutil
except ImportError:
    print("pywin32 is not installed. Please install it with 'pip install pywin32'.")
    sys.exit(1)

# Initialize colorama
try:
    init(autoreset=True)
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import Fore, Style, init
    init(autoreset=True)


def is_valid_ip(ip):
    """Check if the given IP address is valid."""
    try:
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        handle_error(
            ErrorContent.INVALID_IP, 
            ip, 
            ErrorReason.VALUE_ERROR
        )
        return False


def format_event(event):
    """Format event data for easy understanding."""
    try:
        # Convert timestamp correctly
        timestamp = datetime.fromtimestamp(event.TimeGenerated.timestamp()).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        handle_error(
            ErrorContent.TIMESTAMP_ERROR, 
            str(e), 
            ErrorReason.UNKNOWN_ERROR
        )
        timestamp = "Unknown"
    
    try:
        user = event.StringInserts[5] if len(event.StringInserts) > 5 else "Unknown"
    except Exception as e:
        handle_error(
            ErrorContent.USER_INFO_ERROR, 
            str(e), 
            ErrorReason.UNKNOWN_ERROR
        )
        user = "Unknown"
    
    try:
        msg_str = ' '.join(str(m) for m in event.StringInserts)
        ip_match = re.search(r'(\d{1,3}\.){3}\d{1,3}', msg_str)
        src_ip = ip_match.group(0) if ip_match and is_valid_ip(ip_match.group(0)) else "N/A"
    except Exception as e:
        handle_error(
            ErrorContent.IP_EXTRACTION_ERROR, 
            str(e), 
            ErrorReason.UNKNOWN_ERROR
        )
        src_ip = "N/A"
    
    return timestamp, user, src_ip


def display_event_info(timestamp, user, src_ip, event_id, success=True):
    """Print event information based on event ID."""
    color = Fore.GREEN if success else Fore.RED
    status = "Successful login" if success else "Failed login attempt"
    print(f"{color}[{timestamp}] {Style.BRIGHT}{status} detected!")
    print(f"User: {user} | Source IP: {src_ip}")
    print(f"{color}Event ID {event_id}: {status}!")
    print("-" * 70)


def check_user_info():
    """Check and display user information using net user."""
    try:
        result = subprocess.check_output("net user", shell=True).decode('utf-8', errors='ignore')
        print(f"{Fore.CYAN}[INFO] Current User Information:")
        print(result)
    except subprocess.CalledProcessError as e:
        handle_error(
            ErrorContent.COMMAND_EXECUTION_ERROR, 
            str(e), 
            ErrorReason.COMMAND_ERROR
        )
    except PermissionError as e:
        handle_error(
            ErrorContent.PERMISSION_ERROR, 
            str(e), 
            ErrorReason.PERMISSION_DENIED
        )


def monitor_user_activity():
    server = 'localhost'
    log_type = 'Security'

    try:
        hand = win32evtlog.OpenEventLog(server, log_type)
        print(f"{Fore.GREEN}[INFO] Successfully opened the Security event log.")
    except Exception as e:
        if "access is denied" in str(e).lower():
            handle_error(
                ErrorContent.PERMISSION_ERROR, 
                str(e), 
                ErrorReason.PERMISSION_DENIED
            )
        else:
            handle_error(
                ErrorContent.LOG_OPEN_ERROR, 
                str(e), 
                ErrorReason.UNKNOWN_ERROR
            )
        return

    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    login_event_ids = [4624, 4625]

    print(f"{Fore.GREEN}[INFO] Monitoring user activity. Press Ctrl+C to stop.")
    
    try:
        while True:
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            if not events:
                print(f"{Fore.YELLOW}[INFO] No more events to process.")
                break

            for event in events:
                if event.EventID in login_event_ids:
                    timestamp, user, src_ip = format_event(event)
                    if event.EventID == 4624:
                        display_event_info(timestamp, user, src_ip, 4624, success=True)
                    elif event.EventID == 4625:
                        display_event_info(timestamp, user, src_ip, 4625, success=False)
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}[INFO] Monitoring stopped by user.")
    except Exception as e:
        handle_error(
            ErrorContent.LOG_READ_ERROR, 
            str(e), 
            ErrorReason.UNKNOWN_ERROR
        )
    finally:
        try:
            win32evtlog.CloseEventLog(hand)
            print(f"{Fore.GREEN}[INFO] Log handle closed.")
        except Exception as e:
            handle_error(
                ErrorContent.LOG_CLOSE_ERROR, 
                str(e), 
                ErrorReason.UNKNOWN_ERROR
            )

    check_user_info()


if __name__ == "__main__":
    monitor_user_activity()
