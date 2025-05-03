import pyfiglet
import shutil

def version():
    version_str = """
    NO_ONX

    --------------------------------------
    Version: 0.2.8 Beta

    - Update infomation: Check the changelog
    - Platform: Windows 10/11

    Changelog: https://github.com/DevStatesSmp/NO_ONX/blob/NO_ONX/CHANGELOG.md
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

    version_str = "v0.2.4 beta"
    print(" " * (max_line_length - len(version_str)) + f"\033[90m{version_str}\033[0m\n")
    print("\033[96m📖 Usage: python <module_name>.py or nnx <Argument> <...>\033[0m\n")