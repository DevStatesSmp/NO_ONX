import sys
from typing import Optional

class WarningContent:
    PERFORMANCE_WARNING = "Warning: Potential performance issue"
    POTENTIAL_OVERWRITE_WARNING = "Warning: File may be overwritten"
    LOW_DISK_SPACE_WARNING = "Warning: Low disk space"
    CONFIG_WARNING = "Warning: Configuration issue"

class ErrorContent:
    INVALID_OPTION_ERROR = "Invalid options"
    WHEN_RUNNING_ERROR = "Error when running comand"
    MISSING_ARGUMENTS_ERROR = "Error when running command"
    COMPILER_CPP_ERROR = "Error when compiler C++ file"
    READFILE_ERROR = "Error when read file"
    COMPARE_ERROR = "Error when comparing two paths"
    BACKUP_FILE_ERROR = "Error when backup file"
    BACKUP_DIREC_ERROR = "Error when backup directory"
    MODIFY_ERROR = "Error when modify file"
    SCANNING_ERROR = "Error when scanning file"
    MONITORING_ERROR = "Error when watcher path"
    UNSUPPORTEDCOMMAND_ERROR = "Unsupported nnx command"
    MISSING_TYPE_COMMAND = "Error when running command type"
    RESTORE_FILE_DIRECT = "Error when restore file"
    RESTORE_DIREC_ERROR = "Error when restore directory"
    PERMISSION_ERROR = "Error when running command"
    SAVE_RESULT_ERROR = "Error when save result"
    PLUGIN_ERROR = "Error when loading plugin"
    EVENT_READING = "Error when reading event"
    EVENT_LOG = "Error when reading log"

    LOG_OPEN_ERROR = "Error when opening event log"
    LOG_READ_ERROR = "Error when reading event log"
    LOG_CLOSE_ERROR = "Error when closing event log"
    TIMESTAMP_ERROR = "Error when formatting timestamp"
    USER_INFO_ERROR = "Error when extracting user information"
    IP_EXTRACTION_ERROR = "Error when extracting IP address"
    COMMAND_EXECUTION_ERROR = "Error during command execution"
    INVALID_IP = "Invalid IP address"
    LOADING = "Error when loading command"

class ErrorReason:
    # Invalid reasons
    INVALID_TYPE = "Invalid type." # This is also the operation too
    INVALID_PATH = "Invalid path."
    INVALID_FILE = "Invalid file."

    # Missing reasons
    MISSING_TYPE = "Missing type."
    MISSING_ARGUMENTS = "Missing arguments."
    MISSING_ARGUMENTS_NNX = "Missing arguments, Use 'nnx --help' for guidance."
    MISSING_COMPILER_EXE = "Missing .exe file, did you compiler cpp file it?"
    MISSING_PATH ,MISSING_DUPLI_PATH = "Missing path", "Missing first path and second path."
    MISSING_LIB = "Missing required library, use 'pip install -r requirements.txt'."
    PATH_NOT_EXISTS = "Path does not exists."
    PATH_NOT_FOUND = "Path not found."
    FILE_NOT_FOUND = "File not found."
    PERMISSION_DENIED = "Permission denied."
    ACCESS_DENIED = "Access denied."

    # Not exists reason
    MISSING_FILE = "File does not exist."
    MISSING_PATH = "Path does not exist."
    # other reasons
    UNKNOWN_ERROR = "unknown error."
    UNSUPPORTED_COMMAND = "use 'nnx --help' for more information."
    NOT_DIREC_ERROR = "The specified path is not a directory."
    VALUE_ERROR = "Invalid value."
    COMMAND_ERROR = "Invalid command."

    # Cannot reason
    CANNOT_MOVE_FILE = "Cannot move file."
    CANNOT_RENAME_FILE = "Cannot rename file."
    CANNOT_RENAME_DIREC = "Cannot rename directory."
    CANNOT_MOVE_DIREC = "Cannot move directory."
    CANNOT_MODIFY_METADATA = "Cannot modify file metadata."
    CANNOT_CREATE_SYMLINK = "Cannot create symlink."
    CANNOT_DELETE_SYMLINK = "Cannot delete symlink."
    CANNOT_READ_FILE = "Cannot read file."
    CANNOT_WRITE_FILE = "Cannot write file."

    # Not reason
    NOT_FILE = "The specified path is not a file."
    NOT_DIRECTORY = "The specified path is not a directory."

    # FAILED reason
    FAILED_LOADPLUGIN = "Failed to load init"


def handle_error(content: str, value=None, reason: Optional[str] = None, to_stderr: bool = False, exit_code: int = 1) -> None:
    """
    Handles errors by printing a formatted error message and exiting the program.

    Args:
            error_type (str): The main error message, typically from ErrorContent.
            reason (str, optional): Additional reason for the error, typically from ErrorReason.
            details (str, optional): Any extra details to display.
            to_stderr (bool, optional): Whether to print to stderr. Defaults to False.
            exit_code (int, optional): Exit code for sys.exit(). If None, does not exit. Defaults to 1.

    Example:
            handle_error(ErrorContent.WHEN_RUNNING_ERROR, ErrorReason.INVALID_TYPE)
    """

    if isinstance(value, (set, list, tuple)) and len(value) == 1:
        value = next(iter(value))

    message_parts = [f"\033[91m[!] {content}\033[0m"]
    if value is not None:
        message_parts.append(str(value))
    if reason:
        message_parts.append(str(reason))
    if len(message_parts) > 1:
        message = ": ".join(message_parts[:2])
        if len(message_parts) > 2:
            message += f", {', '.join(message_parts[2:])}"
    else:
        message = message_parts[0]

    print(message, file=sys.stderr if to_stderr else sys.stdout)

    if exit_code is not None:
        sys.exit(exit_code)