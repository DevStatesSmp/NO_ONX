import os
import shutil
import requests
import subprocess
from src.utils.getError import handle_error, ErrorContent, ErrorReason
from src.utils.loading_effect import loading_effect
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_FOLDER = os.path.join(BASE_DIR)
DOWNLOAD_FOLDER = PLUGIN_FOLDER

try:
    import rarfile
    import json
except ImportError:
    handle_error(ErrorContent.WHEN_RUNNING_ERROR, "rarfile", ErrorReason.LIB_NOT_FOUND, "Please install it using 'pip install rarfile'.")
    exit(1)

# Plugin Store is cancelled, you should wait a new update or use old way.
PLUGIN_STORE_URL = "https://raw.githubusercontent.com/DevStatesSmp/NNX-Plugin-Store/main/plugins.json" # Change this URL to your plugin store URL
DOWNLOAD_FOLDER = r"src\plugins"

def fetch_plugin_store(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        print(f"[DEBUG] Fetched plugin store data: {data}")
        return data
    except Exception as e:
        handle_error(ErrorContent.WHEN_RUNNING_ERROR, "NNX Plugin Store", ErrorReason.NETWORK_ERROR)
        return None

def download_plugin_rar(plugin, download_folder):
    url = plugin.get("url")
    if not url:
        print(f"Plugin '{plugin.get('name')}' don't have a valid URL.")
        return None

    if not url.lower().endswith(".rar"):
        handle_error(ErrorContent.WHEN_RUNNING_ERROR, {plugin.get('name')}, ErrorReason.INVALID_FILE)
        return None

    os.makedirs(download_folder, exist_ok=True)
    filename = url.split("/")[-1]
    filepath = os.path.join(download_folder, filename)

    loading_effect(f"Downloading plugin... {plugin.get('name')}", 0.5)
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("Download is finished, continue to extract...")
        return filepath
    except Exception as e:
        handle_error(ErrorContent.WHEN_RUNNING_ERROR, {plugin.get('name')}, ErrorReason.NETWORK_ERROR)
        return None

def is_tool_available(tool_name):
    try:
        subprocess.run([tool_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def extract_rar(filepath, extract_to):
    loading_effect("Extracting plugin...", 0.5)
    os.makedirs(extract_to, exist_ok=True)

    if is_tool_available("unrar"):
        cmd = ["unrar", "x", "-y", filepath, extract_to]
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                handle_error(ErrorContent.WHEN_RUNNING_ERROR, {result.stderr.strip()}, ErrorReason.UNKNOWN_ERROR)
                return False
            print("Extract finished...")
            return True
        except Exception as e:
            handle_error(ErrorContent.WHEN_RUNNING_ERROR, {e}, ErrorReason.UNKNOWN_ERROR)
            return False
    elif is_tool_available("7z"):
        cmd = ["7z", "x", filepath, f"-o{extract_to}", "-y"]
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                handle_error(ErrorContent.WHEN_RUNNING_ERROR, {result.stderr.strip()}, ErrorReason.UNKNOWN_ERROR)
                return False
            print("Extract finished.")
            return True
        except Exception as e:
            handle_error(ErrorContent.WHEN_RUNNING_ERROR, {e}, ErrorReason.UNSUPPORTED_COMMAND)
            return False
    else:
        print("Cannot find 'unrar' or '7z' in system PATH. Trying to extract using rarfile library...")
        try:
            with rarfile.RarFile(filepath) as rf:
                rf.extractall(path=extract_to)
            print("Extract finished using rarfile.")
            return True
        except Exception as e:
            handle_error(ErrorContent.WHEN_RUNNING_ERROR, "Plugin extraction", ErrorReason.UNSUPPORTED_COMMAND)
            print("Please install one of these tools or ensure the rar file is not corrupted.")
            print("You can also try to extract the rar file manually.")
            return False

def plugin_install():
    store = fetch_plugin_store(PLUGIN_STORE_URL)
    print(store)
    if not store:
        print("[PLUGINS] Could not load plugin store.")
        return

    plugins = store.get("plugins", [])
    if not plugins:
        handle_error(ErrorContent.WHEN_RUNNING_ERROR, "NNX Plugin Store", ErrorReason.PLUGIN_NOT_FOUND)
        return

    print("List of plugins in the store:")
    for i, p in enumerate(plugins, 1):
        print(f"{i}. {p['name']} (v{p['version']}) - {p['description']}")

    print("\nDo you want to install all plugins? (y/N)")
    answer = input().strip().lower()
    if answer == 'y':
        for plugin in plugins:
            filepath = download_plugin_rar(plugin, DOWNLOAD_FOLDER)
            if filepath:
                folder_name = os.path.splitext(os.path.basename(filepath))[0]
                extract_to = os.path.join(PLUGIN_FOLDER, folder_name)
                if extract_rar(filepath, extract_to):
                    print(f"Plugin '{plugin.get('name')}' installed successfully.\n")
                else:
                    print(f"Failed to extract plugin '{plugin.get('name')}'.\n")
    else:
        print("Installation cancelled.")

def plugin_uninstall(identifier):
    found_plugin_path = None
    found_plugin_info = None

    for plugin_dir in os.listdir(PLUGIN_FOLDER):
        if plugin_dir == "__pycache__" or plugin_dir.startswith("."):
            continue  
        plugin_path = os.path.join(PLUGIN_FOLDER, plugin_dir)
        if not os.path.isdir(plugin_path):
            continue
        
        manifest_path = os.path.join(plugin_path, "plugin.json")
        if not os.path.isfile(manifest_path):
            continue
        
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            handle_error(ErrorContent.WHEN_RUNNING_ERROR, {manifest_path}, {e}, "Invalid JSON Format")
            continue

        plugin_id = data.get("id", "").lower()
        plugin_name = data.get("name", "").lower()
        ident = identifier.lower()

        if ident == plugin_id or ident == plugin_name:
            found_plugin_path = plugin_path
            found_plugin_info = data
            break
    
    if not found_plugin_path:
        handle_error(ErrorContent.WHEN_RUNNING_ERROR, {identifier}, ErrorReason.PLUGIN_NOT_FOUND)
        return
    
    confirm = input(f"Are you sure to uninstall '{found_plugin_info.get('name', identifier)}'? (y/N): ").strip().lower()
    if confirm != "y":
        print("Cancelled uninstalling plugin.")
        return
    
    try:
        shutil.rmtree(found_plugin_path)
        print(f"Plugin '{found_plugin_info.get('name', identifier)}' has been uninstalled successfully.")
    except Exception as e:
        handle_error(ErrorContent.WHEN_RUNNING_ERROR, {found_plugin_info.get('name', identifier)}, ErrorReason.UNKNOWN_ERROR)
        print("Please try to remove the plugin folder manually.")

def list_plugins_with_id(plugin_folder):
    plugins = []
    for foldername in os.listdir(plugin_folder):
        if foldername == "__pycache__" or foldername.startswith("."):
            continue
        folderpath = os.path.join(plugin_folder, foldername)
        if os.path.isdir(folderpath):
            json_path = os.path.join(folderpath, "plugin.json")
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                plugins.append((foldername, data.get("id", ""), data.get("name", "")))
            else:
                plugins.append((foldername, "", "No plugin.json found"))
    return plugins

        