# THIS IS MODULE, DO NOT RUN THIS FILE DIRECTLY

import subprocess
import sys
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from src.utils.getError import handle_error, ErrorContent, ErrorReason

from .monitoring.activity_detective import monitor_user_activity
from .monitoring.security_detective import check_privilege_escalation
from .monitoring.network_detective import networker_detective, is_admin
from .monitoring.sys_health import show_sys_health, show_proc_watch

def get_bin_dir():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.abspath(os.path.join(base_dir, '..'))
    bin_dir = os.path.join(src_dir, '..', 'bin')
    bin_dir = os.path.normpath(bin_dir)
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)
    return bin_dir

def watch_detective(path):
    cpp_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'monitoring', 'watcher_detective.cpp'))
    if not os.path.exists(cpp_file):
        handle_error(ErrorContent.COMPILER_CPP_ERROR, {cpp_file}, ErrorReason.MISSING_FILE)
        sys.exit(1)

    bin_dir = get_bin_dir()
    exe_path = os.path.join(bin_dir, 'detective.exe')  # Windows exe

    if not os.path.exists(exe_path):
        print(f"\n🔨 Compiling {cpp_file}...")
        try:
            subprocess.run(['g++', cpp_file, '-o', exe_path], check=True)
            print("\033[92m[+]\033[0m Compilation successful.")
        except subprocess.CalledProcessError:
            handle_error(ErrorContent.COMPILER_CPP_ERROR, {cpp_file})
            sys.exit(1)

    if not os.path.exists(path):
        handle_error(ErrorContent.MISSING_TYPE_COMMAND, {path}, ErrorReason.INVALID_PATH)
        sys.exit(1)

    print(f"\n📂 Watching: {path}\n")

    try:
        process = subprocess.Popen(
            [exe_path, path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            print(line, end='')

    except FileNotFoundError:
        handle_error(ErrorContent.MISSING_ARGUMENTS_ERROR, {exe_path}, ErrorReason.MISSING_COMPILER_EXE)
    except KeyboardInterrupt:
        print("\n\033[91m[!] Interrupted by user. Exiting...\033[0m")

def process_detective():
    cpp_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'monitoring', 'process_anomaly_detective.cpp'))
    if not os.path.exists(cpp_file):
        handle_error(ErrorContent.COMPILER_CPP_ERROR, {cpp_file}, ErrorReason.MISSING_FILE)
        sys.exit(1)

    bin_dir = get_bin_dir()
    exe_path = os.path.join(bin_dir, 'process_anomaly_detective.exe')  # Windows exe

    if not os.path.exists(exe_path):
        print(f"\n🔨 Compiling {cpp_file}...")
        try:
            subprocess.run([
                'g++', '-std=c++17', '-Wall', '-Wextra', '-o', exe_path, cpp_file,
                '-lole32', '-loleaut32', '-lwbemuuid', '-lpsapi'
            ], check=True)
            print("\033[92m[+]\033[0m Compilation successful.")
        except subprocess.CalledProcessError:
            handle_error(ErrorContent.COMPILER_CPP_ERROR, {cpp_file})
            sys.exit(1)

    print(f"\n🚀 Running {os.path.basename(exe_path)}...\n")

    try:
        process = subprocess.Popen(
            [exe_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in process.stdout:
            print(line, end='')

        process.wait()

    except FileNotFoundError:
        handle_error(ErrorContent.MISSING_ARGUMENTS_ERROR, {exe_path}, ErrorReason.MISSING_COMPILER_EXE)
    except KeyboardInterrupt:
        print("\n\033[91m[!] Interrupted by user. Exiting...\033[0m")

def process_watcher():
    cpp_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'monitoring', 'process_watcher_detective.cpp'))
    if not os.path.exists(cpp_file):
        handle_error(ErrorContent.COMPILER_CPP_ERROR, {cpp_file}, ErrorReason.MISSING_FILE)
        sys.exit(1)

    bin_dir = get_bin_dir()
    exe_path = os.path.join(bin_dir, 'process_watcher_detective.exe')  # Windows exe

    if not os.path.exists(exe_path):
        print(f"\n🔨 Compiling {cpp_file}...")
        try:
            subprocess.run([
                'g++', '-std=c++17', '-Wall', '-Wextra', '-o', exe_path, cpp_file,
                '-lole32', '-loleaut32', '-lwbemuuid', '-lpsapi'
            ], check=True)
            print("\033[92m[+]\033[0m Compilation successful.")
        except subprocess.CalledProcessError:
            handle_error(ErrorContent.COMPILER_CPP_ERROR, {cpp_file})
            sys.exit(1)

    print(f"\n🚀 Running {os.path.basename(exe_path)}...\n")

    try:
        process = subprocess.Popen(
            [exe_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in process.stdout:
            print(line, end='')

        process.wait()

    except FileNotFoundError:
        handle_error(ErrorContent.MISSING_ARGUMENTS_ERROR, {exe_path}, ErrorReason.MISSING_COMPILER_EXE)
    except KeyboardInterrupt:
        print("\n\033[91m[!] Interrupted by user. Exiting...\033[0m")

def activity_detective():
    try:
        monitor_user_activity()
    except Exception as e:
        print(f"\033[91m[!] Error in activity_detective:\033[0m {e}")

def security_detective():
    try:
        check_privilege_escalation()
    except Exception as e:
        print(f"\033[91m[!] Error in security_detective:\033[0m {e}")

def network_detective():
    if not is_admin():
        print("\033[91m[!]\033[0m You are not running this program as Administrator.")
        print("Some features may not work properly without admin privileges.")
        ans = input("Do you want to continue anyway? (y/N): ").strip().lower()
        if ans != 'y':
            print("Exiting... Please run as Administrator/root.")
            sys.exit(1)
    networker_detective()

def system_health():
    while True:
        print("Choose command:")
        print("1. System Health Report")
        print("2. Process Watch")
        print("0. Exit")
        cmd = input("Enter choice: ").strip()

        if cmd == '1':
            show_sys_health()
        elif cmd == '2':
            try:
                top_n = int(input("How many top processes to show? (default 5): ") or "5")
            except:
                top_n = 5
            show_proc_watch(top_n)
        elif cmd == '0':
            print("Exiting...")
            break
        else:
            print("Invalid command. Try again.\n")
            handle_error(ErrorContent.WHEN_RUNNING_ERROR, cmd, ErrorReason.INVALID_TYPE)