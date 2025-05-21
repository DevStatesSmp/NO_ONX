# THIS IS MODULE, DO NOT RUN THIS FILE DIRECTLY

import shutil
import os
import time
import logging
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from src.utils.getError import handle_error, ErrorContent, ErrorReason

logging.basicConfig(filename='backup.log', level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')

current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
backup_dir = os.path.join(current_dir, "backup")

os.makedirs(backup_dir, exist_ok=True)

def backup_file(source):
    try:
        if not os.path.exists(source):
            raise FileNotFoundError(f"File not found: {source}")
        
        backup_location = os.path.join(backup_dir, os.path.basename(source))
        
        if os.path.exists(backup_location):
            logging.info(f"File already backed up: {backup_location}")
            print(f"File already backed up: {backup_location}")
            return

        shutil.copy(source, backup_location)
        logging.info(f"Backup successful: {source} -> {backup_location}")
        print(f"Backup successful: {source} -> {backup_location}")
        
    except Exception as e:
        logging.error(f"Error during backup: {e}")
        handle_error(ErrorContent.BACKUP_FILE_ERROR, str(e), reason=ErrorReason.UNKNOWN_ERROR)

def restore_backup(backup_location, restore_location):
    try:
        if not os.path.exists(backup_location):
            raise FileNotFoundError(f"Backup file not found: {backup_location}")
        
        shutil.copy(backup_location, restore_location)
        logging.info(f"Restore successful: {backup_location} -> {restore_location}")
        print(f"Restore successful: {backup_location} -> {restore_location}")
    except Exception as e:
        logging.error(f"Error during restore: {e}")
        handle_error(ErrorContent.RESTORE_FILE_ERROR, str(e), reason=ErrorReason.UNKNOWN_ERROR)

def backup_directory(source_dir):
    try:
        if not os.path.isdir(source_dir):
            raise NotADirectoryError(f"Source is not a directory: {source_dir}")

        backup_location = os.path.join(backup_dir, os.path.basename(source_dir))
        
        if os.path.exists(backup_location):
            shutil.rmtree(backup_location)

        shutil.copytree(source_dir, backup_location)
        logging.info(f"Backup successful: {source_dir} -> {backup_location}")
        print(f"Backup successful: {source_dir} -> {backup_location}")
    except Exception as e:
        logging.error(f"Error during backup: {e}")
        handle_error(ErrorContent.BACKUP_DIREC_ERROR, str(e), reason=ErrorReason.NOT_A_DIRECTORY)

def restore_directory(backup_location, restore_location):
    try:
        if not os.path.exists(backup_location):
            raise FileNotFoundError(f"Backup directory not found: {backup_location}")
        
        if os.path.exists(restore_location):
            shutil.rmtree(restore_location)

        shutil.copytree(backup_location, restore_location)
        logging.info(f"Restore successful: {backup_location} -> {restore_location}")
        print(f"Restore successful: {backup_location} -> {restore_location}")
    except Exception as e:
        logging.error(f"Error during restore: {e}")
        handle_error(ErrorContent.RESTORE_DIREC_ERROR, str(e), reason=ErrorReason.UNKNOWN_ERROR)

def backup_file_with_timestamp(source):
    try:
        if not os.path.exists(source):
            raise FileNotFoundError(f"File not found: {source}")

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_location = os.path.join(backup_dir, f"{timestamp}_{os.path.basename(source)}")

        shutil.copy(source, backup_location)
        logging.info(f"Backup successful with timestamp: {source} -> {backup_location}")
        print(f"Backup successful: {source} -> {backup_location}")
    except Exception as e:
        logging.error(f"Error during backup: {e}")
        handle_error(ErrorContent.BACKUP_FILE_ERROR, str(e), reason=ErrorReason.UNKNOWN_ERROR)

def backup_multiple_files(files):
    for file in files:
        backup_file(file)

def backup_multiple_directories(directories):
    for directory in directories:
        backup_directory(directory)

def clean_old_backups(days=30):
    try:
        for filename in os.listdir(backup_dir):
            file_path = os.path.join(backup_dir, filename)
            if os.path.getmtime(file_path) < time.time() - days * 86400:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
                logging.info(f"Deleted old backup: {file_path}")
                print(f"Deleted old backup: {file_path}")
    except Exception as e:
        logging.error(f"Error during cleaning old backups: {e}")
        handle_error(ErrorContent.BACKUP_DIREC_ERROR, str(e), reason=ErrorReason.UNKNOWN_ERROR)
