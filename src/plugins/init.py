import os
import importlib
import sys

from src.utils.loading_effect import loading_effect
from src.utils.getError import *

plugin_dir = os.path.dirname(__file__)

loaded_plugins = {}

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
        loading_effect("Loading plugin init (Required)...")
        init_module = importlib.import_module("src.plugins.init")
        loaded_plugins["init"] = init_module
        print("[PLUGIN] Loaded: init (Required)")
    except Exception as e:
        handle_error(
            ErrorContent.PLUGIN_ERROR,
            {"exception": str(e), "traceback": getattr(e, '__traceback__', None)},
            ErrorReason.FAILED_LOADPLUGIN
        )
        sys.exit(1) 

    plugin_files = find_plugins(plugin_dir)


    if plugin_files:
        loading_effect("Loading plugins...\n")

    for module_name in plugin_files:
        plugin_name = module_name.split('.')[-1]
        if plugin_name == "init":
            continue
        try:
            module = importlib.import_module(f"src.plugins.{module_name}")
            loaded_plugins[plugin_name] = module
            print(f"[PLUGIN] Loaded: {plugin_name}")
        except Exception as e:
            handle_error(ErrorContent.PLUGIN_ERROR, plugin_name, str({e}), "Failed to load")

    clear_line()

def get_plugin(plugin_name):
    return loaded_plugins.get(plugin_name)

def list_plugins():
    return [p for p in loaded_plugins.keys() if p != "init"]

def ask_use_plugin(plugin_name):
    answer = input(f"Do you want to use '{plugin_name}'? (y/N): ").strip().lower()
    return answer == 'y'