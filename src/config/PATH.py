import sys
import os

# Determine the base directory for the plugin path
# This handles both frozen applications (like PyInstaller) and normal Python scripts
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Define the plugin directory relative to the base directory
# This allows the plugin directory to be located in the src/plugins folder

# Path
PLUGIN_DIR = os.path.join(BASE_DIR, 'src', 'plugins')