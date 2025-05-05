import pyfiglet
import shutil
from src.utils.config import SETTINGS


def version():
    version_str = f"""
    NO_ONX

    --------------------------------------
    Version: {SETTINGS["NNX_VERSION"]}

    - Update infomation: Check the changelog
    - Platform: Windows 10/11

    Changelog: https://github.com/DevStatesSmp/NO_ONX/blob/main/CHANGELOG.md
    For bug reports or feedback, please contact: https://t.me/+-hUpHRhvj9wyYmE1
    """

    print(f"\033[90mVersion:\033[0m {version_str}")

# Banner tool
def banner():
    term_width = shutil.get_terminal_size().columns
    ascii = pyfiglet.figlet_format("NO_ONX", font="slant")
    banner_lines = ascii.splitlines()
    max_line_length = max(len(line) for line in banner_lines)

    for line in banner_lines:
        print(f"\033[92m{line.center(term_width)}\033[0m")

    version_str = SETTINGS["NNX_VERSION"]
    print(" " * (max_line_length - len(version_str)) + f"\033[90m{version_str}\033[0m\n")
    print("\033[96m📖 Usage: nnx <Argument> <...>\033[0m\n")