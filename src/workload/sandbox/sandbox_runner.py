import subprocess
import os
import tempfile
import shutil
import psutil
import logging
import time
import threading
import hashlib
import sys

logging.basicConfig(level=logging.INFO)

def build_cmd(script_name, config):
    cmd = [sys.executable, script_name]
    if config.get("args"):
        cmd.extend(config["args"])
    if config.get("limits", {}).get("memory"):
        cmd.append(f"--memory={config['limits']['memory']}")
    if config.get("limits", {}).get("cpu"):
        cmd.append(f"--cpu={config['limits']['cpu']}")
    return cmd

def hash_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

def snapshot_files(directory):
    file_info = {}
    for root, dirs, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            rel_path = os.path.relpath(path, directory)
            file_info[rel_path] = {
                "size": os.path.getsize(path),
                "hash": hash_file(path)
            }
    return file_info

def monitor_resources(proc, stats, interval=0.1):
    try:
        p = psutil.Process(proc.pid)
        while proc.poll() is None:
            with p.oneshot():
                stats["cpu"].append(p.cpu_percent(interval=interval))
                stats["mem"].append(p.memory_info().rss)
                stats["io"].append(p.io_counters()._asdict() if hasattr(p, "io_counters") else {})
            time.sleep(interval)
    except Exception:
        pass

def execute(target_file: str, config: dict):
    if config is None:
        config = {}

    timeout = config.get("limits", {}).get("timeout", 10)
    env = os.environ.copy()
    if config.get("env"):
        env.update({k: str(v) for k, v in config["env"].items()})

    if not os.path.isfile(target_file):
        logging.error(f"Target file does not exist: {target_file}")
        return {"stdout": "", "stderr": f"Target file does not exist: {target_file}", "returncode": -1}

    with tempfile.TemporaryDirectory(prefix="nnx_private_") as sandbox_dir:
        script_name = os.path.basename(target_file)
        sandbox_script_path = os.path.join(sandbox_dir, script_name)

        try:
            shutil.copy(os.path.abspath(target_file), sandbox_script_path)
        except Exception as e:
            logging.error(f"Failed to copy file: {e}")
            return {"stdout": "", "stderr": f"Failed to copy file: {e}", "returncode": -1}

        if not os.path.isfile(sandbox_script_path):
            logging.error(f"Script not found in sandbox: {sandbox_script_path}")
            return {"stdout": "", "stderr": f"Script not found in sandbox: {sandbox_script_path}", "returncode": -1}

        cmd = build_cmd(script_name, config)
        logging.info(f"Executing command: {cmd} in {sandbox_dir}")

        before_files = snapshot_files(sandbox_dir)
        before_procs = set(p.pid for p in psutil.process_iter())
        before_conns = psutil.net_connections()

        stats = {"cpu": [], "mem": [], "io": []}
        start_time = time.time()

        try:
            proc = subprocess.Popen(
                cmd,
                cwd=sandbox_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            monitor_thread = threading.Thread(target=monitor_resources, args=(proc, stats))
            monitor_thread.start()
            try:
                stdout, stderr = proc.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                proc.kill()
                stdout, stderr = proc.communicate()
                logging.warning("Timeout expired")
                return {"stdout": stdout, "stderr": "Timeout expired", "returncode": -1}
            finally:
                monitor_thread.join()
        except FileNotFoundError as e:
            logging.error(f"FileNotFoundError: {str(e)}")
            return {"stdout": "", "stderr": f"FileNotFoundError: {str(e)}", "returncode": -1}
        except Exception as e:
            logging.error(f"Execution failed: {e}")
            return {"stdout": "", "stderr": f"Execution failed: {e}", "returncode": -1}

        end_time = time.time()

        after_files = snapshot_files(sandbox_dir)
        file_changes = {
            "created": [],
            "deleted": [],
            "modified": []
        }
        for f in after_files:
            if f not in before_files:
                file_changes["created"].append(f)
            elif after_files[f]["hash"] != before_files[f]["hash"]:
                file_changes["modified"].append(f)
        for f in before_files:
            if f not in after_files:
                file_changes["deleted"].append(f)

        after_procs = set(p.pid for p in psutil.process_iter())
        new_pids = after_procs - before_procs
        proc_tree = []
        for pid in new_pids:
            try:
                p = psutil.Process(pid)
                proc_tree.append({
                    "pid": pid,
                    "name": p.name(),
                    "cmdline": p.cmdline(),
                })
            except Exception:
                continue

        after_conns = psutil.net_connections()
        new_conns = [c for c in after_conns if c not in before_conns]

        usage_report = {
            "cpu_percent": stats["cpu"],
            "mem_rss": stats["mem"],
            "io": stats["io"],
            "duration_sec": end_time - start_time
        }

        logging.info(f"Return code: {proc.returncode}")
        logging.debug(f"STDERR: {stderr}")
        logging.debug(f"STDOUT: {stdout}")
        logging.debug(f"New processes: {proc_tree}")
        logging.debug(f"New network connections: {new_conns}")
        logging.debug(f"File changes: {file_changes}")
        logging.debug(f"Resource usage: {usage_report}")

        return {
            "stdout": stdout,
            "stderr": stderr,
            "returncode": proc.returncode,
            "processes": proc_tree,
            "network": [str(c) for c in new_conns],
            "file_changes": file_changes,
            "resource_usage": usage_report,
            "env_used": env
        }
