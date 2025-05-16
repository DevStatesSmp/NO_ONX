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


def banner():
    print("\n")

    term_width = shutil.get_terminal_size().columns
    ascii_banner = [
        "███╗   ██╗ ████╗             ██████╗ ███╗   ██╗██╗  ██╗",
        "████╗  ██║██╔══██╗          ██╔═══██╗████╗  ██║╚██╗██╔╝",
        "██╔██╗ ██║██║  ██║          ██║   ██║██╔██╗ ██║ ╚███╔╝",
        "██║╚██╗██║██║  ██║          ██║   ██║██║╚██╗██║ ██╔██╗",
        "██║ ╚████║╚█████╔╝█████████╗╚██████╔╝██║ ╚████║██╔╝ ██╗",
        "╚═╝  ╚═══╝ ╚════╝ ╚════════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝"
    ]

    # Calculate left padding for centering the banner block as a whole
    banner_width = max(len(line) for line in ascii_banner)
    left_padding = max((term_width - banner_width) // 2, 0)

    for line in ascii_banner:
        print(f"\033[38;5;208m{' ' * left_padding}{line}\033[0m")

    version_str = SETTINGS["NNX_VERSION"]
    print(f"\033[90m{' ' * (left_padding + banner_width - len(version_str))}{version_str}\033[0m\n")
    print("\033[96m📖 Usage: nnx <argument> [...]\033[0m\n")
