# Plugins

This folder contains plugins designed to **modify or extend** the functionality of the main application.  
You can use plugins to add custom features or make personal adjustments as needed.

## How to Use Plugins

1. Place your plugin files (Python scripts) in this folder.  
2. Each plugin should contain a function named `execute()` that will be called when the plugin is loaded.  
3. Check out the **`example_module.py`** file for a template on how to create a new plugin.  

### Example Usage

To list available plugins, use:
```bash
nnx --list_plugins # also you can use --plugins
python noonx.py --list_plugins # This command for testing

# To use the plugin, use:
nnx --plugin 
python noonx.py --list_plugin # This command for testing
```