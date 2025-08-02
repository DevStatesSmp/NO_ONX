from src.utils.getError import handle_error, ErrorContent, ErrorReason
import hashlib
import os

def get_file_hash(path: str, hash_type: str = "sha256") -> str:
    """
    Calculate the hash of a file using the specified hash algorithm.
    """
    BUF_SIZE = 8192
    hash_func = hashlib.sha256() if hash_type == "sha256" else hashlib.md5()

    try:
        with open(path, 'rb') as f:
            while True:
                chunk = f.read(BUF_SIZE)
                if not chunk:
                    break
                try:
                    hash_func.update(chunk)
                except Exception as chunk_err:
                    handle_error(ErrorContent.SCANNING_ERROR, {"file_path": path, "exception": str(chunk_err)}, ErrorReason.READ_ERROR)
                    return ""
    except FileNotFoundError as e:
        handle_error(ErrorContent.SCANNING_ERROR, {"file_path": path, "exception": str(e)}, ErrorReason.FILE_NOT_FOUND)
        return ""
    except PermissionError as e:
        handle_error(ErrorContent.SCANNING_ERROR, {"file_path": path, "exception": str(e)}, ErrorReason.CANNOT_READ_FILE)
        return ""
    except Exception as e:
        handle_error(ErrorContent.SCANNING_ERROR, {"file_path": path, "exception": str(e)}, ErrorReason.UNKNOWN_ERROR)
        return ""

    return hash_func.hexdigest()
