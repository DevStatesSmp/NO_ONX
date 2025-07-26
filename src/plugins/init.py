import os
import importlib
import sys
import json

from src.utils.loading_effect import loading_effect
from src.utils.getError import *
from src.plugins.plugins_manager import list_plugins_with_id

plugin_dir = os.path.join(os.path.dirname(__file__), "..", "plugins")

loaded_plugins = {}
loaded_successfully = []

def clear_line():
    print('\r' + ' ' * 50 + '\r', end='', flush=True)

def find_plugins(directory):
    plugin_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and file.lower() not in ["__init__.py", "readme.md"]:
                relative_path = os.path.relpath(os.path.join(root, file), plugin_dir)
                module_name = relative_path.replace(os.sep, ".")[:-3]
                plugin_files.append(module_name)
    return plugin_files
    
def load_plugins():
    try:
        loading_effect("Loading Plugins init (Required)...")
        init_module = importlib.import_module("src.plugins.init")
        loaded_plugins["init"] = init_module
        print("[CORE] Loaded: init")
        loading_effect("Loading Plugins Manager... (Required)")

        plugins_manager_module = importlib.import_module("src.plugins.plugins_manager")
        loaded_plugins["plugins_manager"] = plugins_manager_module
        print("[CORE] Loaded: plugins_manager")
    except Exception as e:
        handle_error(ErrorContent.PLUGIN_ERROR, {"exception": str(e), "traceback": getattr(e, '__traceback__', None)}, ErrorReason.FAILED_LOADPLUGIN)
        sys.exit(1) 

    plugin_files = find_plugins(plugin_dir)
    if plugin_files:
        loading_effect("Loading plugins...", duration=1)
    plugins = list_plugins_with_id(plugin_dir)

    for module_name in plugin_files:
        plugin_name = module_name.split('.')[-1]
        if plugin_name.lower() in ("init", "plugins_manager"):
            continue
        try:
            loading_effect(f"Loading: {plugin_name}...", 0.3)
            module = importlib.import_module(f"src.plugins.{module_name}")
            loaded_plugins[plugin_name.lower()] = module
            loaded_successfully.append(plugin_name)
            # print(f"[PLUGIN] Loaded: {plugin_name}")
            clear_line()
        except Exception as e:
            clear_line()
            handle_error(ErrorContent.PLUGIN_ERROR, plugin_name, str({e}), "Failed to load")

    valid_plugins = [
        (foldername, pid, pname)
        for foldername, pid, pname in plugins
        if foldername.lower() not in ("init", "plugins_manager")
    ]

    if not valid_plugins:
        print("\n[PLUGINS] No avaiable plugins found.\n")
        return
    else:   
        print("\n[PLUGINS] Available Plugins:")
        for foldername, pid, pname in plugins:
            if foldername in ("init", "plugins_manager"):
                continue
            version = ""
            json_path = os.path.join(plugin_dir, foldername, "plugin.json")
            if os.path.exists(json_path):
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    version = data.get("version", "")
                except Exception:
                    version = ""
            if version:
                print(f"- {foldername} (v{version})")
            else:
                print(f"- {foldername}")

    print()
    clear_line()

def get_plugin(plugin_name):
    return loaded_plugins.get(plugin_name.lower())

def list_plugins():
    return [p for p in loaded_plugins.keys() if p not in ("init", "plugins_manager")]

def ask_use_plugin(plugin_name):
    answer = input(f"Do you want to use '{plugin_name}'? (y/N): ").strip().lower()
    return answer == 'y'

plugin_files = find_plugins(plugin_dir)