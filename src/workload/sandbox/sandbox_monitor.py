import subprocess

def monitor_process(cmd, timeout=30):
    trace_cmd = ["strace", "-f", "-e", "trace=open,connect,execve", *cmd]

    try:
        result = subprocess.run(
            trace_cmd,
            capture_output=True,
            timeout=timeout,
            text=True
        )
        return {
            "trace": result.stderr.splitlines()
        }
    except subprocess.TimeoutExpired:
        return {
            "trace": ["[TIMEOUT]"],
        }