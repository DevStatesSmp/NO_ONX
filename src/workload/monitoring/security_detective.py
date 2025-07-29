import win32evtlog
import win32evtlogutil
import re
import logging
from colorama import init, Fore, Style

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from src.utils.getError import handle_error, ErrorContent, ErrorReason

# Initialize colorama
init(autoreset=True)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def check_privilege_escalation():
    server = 'localhost'
    log_type = 'Security'

    # Common Windows privilege escalation event IDs
    escalation_event_ids = {4672, 4673, 4674, 4624, 4625}

    # Improved regex patterns
    escalation_patterns = [
        r'Administrator',
        r'Privilege Use',
        r'Elevated',
        r'sudo',
        r'Special privileges assigned to new logon',
        r'Logon Type:\s*2|10',  # Interactive or remote interactive logon
    ]

    try:
        hand = win32evtlog.OpenEventLog(server, log_type)
        logging.info(Fore.GREEN + 'Successfully opened the Security event log.')
    except Exception as e:
        if hasattr(e, 'winerror') and e.winerror == 1314:
            logging.error(Fore.RED + f'Unable to open event log: (1314, "OpenEventLogW", "A required privilege is not held by the client.")')
            logging.error(Fore.YELLOW + 'Access denied: Run the script as an administrator.')
            handle_error(ErrorContent.EVENT_LOG, {'server': server, 'log_type': log_type}, ErrorReason.ACCESS_DENIED)
        else:
            logging.error(Fore.RED + f'Failed to open event log: {e}')
            handle_error(ErrorContent.EVENT_LOG, {'server': server, 'log_type': log_type}, ErrorReason.UNKNOWN_ERROR)
        return

    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    while True:
        try:
            events = win32evtlog.ReadEventLog(hand, flags, 0)
        except Exception as e:
            if hasattr(e, 'winerror') and e.winerror == 1314:
                logging.error(Fore.RED + f'Unable to read event log: (1314, "ReadEventLogW", "A required privilege is not held by the client.")')
                logging.error(Fore.YELLOW + 'Access denied: Run the script as an administrator.')
                handle_error(ErrorContent.EVENT_READING, {'server': server, 'log_type': log_type}, ErrorReason.ACCESS_DENIED)
            else:
                logging.error(Fore.RED + f'Failed to read event log: {e}')
                handle_error(ErrorContent.EVENT_READING, {'server': server, 'log_type': log_type}, ErrorReason.UNKNOWN_ERROR)
            break

        if not events:
            logging.info(Fore.YELLOW + 'No more events to process.')
            break

        for event in events:
            if event.EventID not in escalation_event_ids:
                continue
            message = event.StringInserts
            if message:
                msg_str = ' '.join(str(m) for m in message)
                for pattern in escalation_patterns:
                    if re.search(pattern, msg_str, re.IGNORECASE):
                        logging.warning(Fore.RED + Style.BRIGHT + 'Privilege Escalation Attempt Detected!')
                        logging.info(Fore.CYAN + f'EventID: {event.EventID}')
                        logging.info(Fore.CYAN + f'Source: {event.SourceName}')
                        logging.info(Fore.CYAN + f'Time Generated: {event.TimeGenerated}')
                        logging.info(Fore.CYAN + f'Message: {msg_str}\n')

    try:
        win32evtlog.CloseEventLog(hand)
        logging.info(Fore.GREEN + 'Event log closed.')
    except Exception as e:
        logging.error(Fore.RED + f'Error closing event log: {e}')
        handle_error(ErrorContent.EVENT_LOG, {'server': server, 'log_type': log_type}, ErrorReason.UNKNOWN_ERROR)
