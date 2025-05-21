# Warning

**Do not delete this folder file.**  
You are only allowed to edit the contents within this folder. Deleting it may cause critical issues in the project.


def watch_detective(path):
    cpp_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'monitoring', 'watcher_detective.cpp'))
    if not os.path.exists(cpp_file):
        print(f"[!] Error: '{cpp_file}' not found.")
        sys.exit(1)

    bin_dir = get_bin_dir()
    exe_path = os.path.join(bin_dir, 'detective')

    if not os.path.exists(exe_path):
        print(f"\n🔨 Compiling {cpp_file}...")
        try:
            subprocess.run(['g++', cpp_file, '-o', exe_path], check=True)
            print("[+] Compilation successful.")
        except subprocess.CalledProcessError:
            print("[!] Compilation failed. Please check for errors in the C++ file.")
            sys.exit(1)

    if not os.path.exists(path):
        print("[!] Invalid path. Exiting.")
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
        print(f"[!] Error: '{exe_path}' binary not found. Did you compile it?")
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Exiting...")

def process_detective():
    cpp_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'monitoring', 'process_anomaly_detective.cpp'))
    if not os.path.exists(cpp_file):
        print(f"[!] Error: '{cpp_file}' not found.")
        sys.exit(1)

    bin_dir = get_bin_dir()
    exe_path = os.path.join(bin_dir, 'process_anomaly_detective.exe')

    if not os.path.exists(exe_path):
        print(f"\n🔨 Compiling {cpp_file}...")
        try:
            subprocess.run([
                'g++', '-std=c++17', '-Wall', '-Wextra', '-o', exe_path, cpp_file,
                '-lole32', '-loleaut32', '-lwbemuuid', '-lpsapi'
            ], check=True)
            print("[+] Compilation successful.")
        except subprocess.CalledProcessError:
            print("[!] Compilation failed. Please check for errors in the C++ file.")
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
        print(f"[!] Error: '{exe_path}' binary not found. Did you compile it?")
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Exiting...")