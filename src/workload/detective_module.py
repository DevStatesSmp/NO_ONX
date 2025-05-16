import subprocess
import sys
import os

from .monitoring.activity_detective import monitor_user_activity
from .monitoring.security_detective import check_privilege_escalation
from .monitoring.network_detective import networker_detective, is_admin
from .monitoring.sys_health import sys_health

def watch_detective(path):
    # Get path to C++ source code
    cpp_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'monitoring', 'watcher_detective.cpp'))

    # Check if the C++ file exists
    if not os.path.exists(cpp_file):
        print(f"[!] Error: '{cpp_file}' not found.")
        sys.exit(1)

    # Compile the C++ file (if not already compiled)
    if not os.path.exists('./detective'):
        print(f"\n🔨 Compiling {cpp_file}...")
        try:
            subprocess.run(['g++', cpp_file, '-o', 'detective'], check=True)
            print("[+] Compilation successful.")
        except subprocess.CalledProcessError:
            print("[!] Compilation failed. Please check for errors in the C++ file.")
            sys.exit(1)

    # Validate the directory path
    if not os.path.exists(path):
        print("[!] Invalid path. Exiting.")
        sys.exit(1)

    print(f"\n📂 Watching: {path}\n")

    # Run the C++ binary (detective)
    try:
        process = subprocess.Popen(
            ['./detective', path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Display the output of the C++ program
        for line in process.stdout:
            print(line, end='')

    except FileNotFoundError:
        print("[!] Error: 'detective' binary not found. Did you compile it?")
        print("    Try: g++ -o detective no_onx_watcher.cpp")
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Exiting...")

def activity_detective():
    try:
        monitor_user_activity()
    except Exception as e:
        print(f"[!] Error in activity_detective: {e}")

def security_detective():
    try:
        check_privilege_escalation()
    except Exception as e:
        print(f"[!] Error in security_detective: {e}")

def network_detective():
    if not is_admin():
        print("[!] You are not running this program as Administrator.")
        print("Some features may not work properly without admin privileges.")
        ans = input("Do you want to continue anyway? (y/N): ").strip().lower()
        if ans != 'y':
            print("Exiting... Please run as Administrator/root.")
            sys.exit(1)
    networker_detective()

def system_health():
    sys_health()
